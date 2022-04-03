import express from "express"
import bodyParser from  'body-parser'


const app = express()
const PORT = 5013

app.use(bodyParser.json({
    verify : (req, res, buf, encoding) => {
    try {
        JSON.parse(buf);
    } catch(e) {
        res.status(404).send('invalid JSON');
    }
    }
}))

// Import the functions you need from the SDKs you need

import { initializeApp } from "firebase/app";
import {
    getFirestore,doc,updateDoc,arrayUnion,setDoc,getDoc, deleteDoc
} from 'firebase/firestore';

const firebaseConfig = {
    apiKey: "AIzaSyDUFLuQ-Ct2g1Ymii1F6kTfsvoHlIT_zQs",
    authDomain: "cocktailogy-accounts.firebaseapp.com",
    databaseURL: "https://cocktailogy-accounts-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "cocktailogy-accounts",
    storageBucket: "cocktailogy-accounts.appspot.com",
    messagingSenderId: "841366379363",
    appId: "1:841366379363:web:25d3f414fbb421675fd156",
    measurementId: "G-CTM3R9DP0F"
  };

  // Initialize Firebase
const firebase_app = initializeApp(firebaseConfig);

const db = getFirestore(firebase_app)
/////////////////////////////////////////////////////////////////////////////////////////////////////
async function writeUserData(account_id,account_name,email,shipping_add){
    var ref = doc(db,"users",account_id)
    try{
        await setDoc(ref,{
            account_name: account_name,
            email : email,
            shipping_add: shipping_add,
            order_history : []
        })
        console.log("success")
        return true
    }
    catch(e){
        return false
    }
}

app.post('/account/:account_id', async (req,res) => {
    let account_id=req.params.account_id
    console.log(Object.keys(req.body).length)

    if (Object.keys(req.body).length != 3){
        return res.status(400).json({
            "code": 400,
            "data": `Too few arguments only ${Object.keys(req.body).length}, need 3`
        })
    }

    let account_name=req.body.account_name
    let email=req.body.email
    let shipping_add = req.body.shipping_add



    let check = await getUserData(account_id)

    if(check){
        return res.status(400).json({
            "code": 400,
            "data": "User Already Exists"
        })
    }

    const result = await writeUserData(account_id,account_name,email,shipping_add)

    if (result){
        res.status(201).json({
            "code": 201,
            "data": "Created account with data"
        })
    }
    else {
        res.status(400).json({
            "code": 400,
            "data": result
        })
    }      
})
///////////////////////////////////////////////////////////
async function getUserData(account_id){
    try{
        let ref = doc(db,"users",account_id)
        const docsnap = await getDoc(ref)
        if (docsnap.exists()){
            return docsnap.data()
        }
    }
    catch(e){
        return false
    }
}


app.get('/account/:account_id', async (req,res) => {
    let account_id=req.params.account_id 
    let result = await getUserData(account_id)

    if (result){
        result['account_id'] = account_id
        res.status(201).json({
            "code": 201,
            "data": result
        })
    }
    else{
        return res.status(400).json({
            "code": 400,
            "data": "No User Found"
        })
    }   
})
/////////////////////////////////////////////////////////////////

async function updateUserData(account_id,email=null,order_info=null,shipping_add=null){
    try{
        let ref = doc(db,"users",account_id)
        if (email != null){
            await updateDoc(ref,{
                email: email,
            })
        }
        if (shipping_add != null){
            await updateDoc(ref,{
                shipping_add: shipping_add,
            })
        }
        if (order_history != null){
            await updateDoc(ref,{
                order_history: arrayUnion({
                    order_info
                }),
            })
        }        
        return true
    }
    catch(e){
        return e
    }
}


app.put('/account/:account_id', async (req,res) => {
    let account_id = req.params.account_id
    let update_info = Object.keys(req.body)
    
    let email = req.body.email
    let order_info = req.body.order_history
    let shipping_add = req.body.shipping_add

    let result = await updateUserData(account_id,email,order_info,shipping_add)

    if (result != true){
        res.status(201).json({
            "code": 201,
            "data": "Updated with updated data"
        })
    }
    else {
        res.status(400).json({
            "code": 400,
            "data": result
        })
    }      

})
////////////////////////////////////////////////////////////////////////////////////

async function deleteUserData(account_id){
    try{
        let ref = doc(db,"users",account_id)
        await deleteDoc(ref)
        return true
    }
    catch(e){
        return e
    }
}

app.delete('/account/:account_id', async (req,res) => {
    let account_id=req.params.account_id 

    let check = await getUserData(account_id)
    if(!check){
        return res.status(400).json({
            "code": 400,
            "data": "User Dosent Exist"
        })
    }
    
    let delete_res = await deleteUserData(account_id)
    
    if( delete_res == true){
        return res.status(200).json({
            "code": 200,
            "data": "User Deleted"
        })
    }
    else {
        return res.status(400).json({
            "code": 400,
            "data": delete_res
        })
    }

})




app.listen(PORT, () => console.log(`Listening On http://localhost:${5013}`))
