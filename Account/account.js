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

import {getDatabase,child,set,ref,update,remove, get}
from "firebase/database"

const db = getDatabase(firebase_app)

async function writeUserData(account_id,account_name,email,shipping_add){
    try{
        await set(ref(db,'users/' + account_id),{
            account_name: account_name,
            email : email,
            shipping_add: shipping_add
        })
        return true
    }
    catch(e){
        return "cannot add document"
    }   
}


app.get('/',(req,res) => {
    console.log("TEST")

    res.send('Hello from homepage')
})

app.get('/account', (req,res) => {

})


app.post('/account/:account_id', async (req,res) => {
    let account_id=req.params.account_id
    console.log(req.body)
    let account_name=req.body.account_name
    let email=req.body.email
    let shipping_add = req.body.shipping_add
    const result = await writeUserData(account_id,account_name,email,shipping_add)

    if (result){
        res.status(201).json({
            "code": 201,
            "data": "Updated with new data"
        })
    }
    else {
        res.status(400).json({
            "code": 400,
            "data": result
        })
    }      
})


app.get('/account/:account_id', async (req,res) => {
    let account_id=req.params.account_id
    const dbref = ref(db) 
    try{
        await get(child(dbref,`users/${account_id}`)).then((snapshot)=>{
            if (snapshot.exists()){
                return res.send(snapshot.toJSON())
            }
            else{
                return res.send(false)
            }
        })
    }
    catch(e){
        return res.send("unsuccesful" + e)
    }   
})
// app.get('/account', async (req,res) => {

// })




app.listen(PORT, () => console.log(`Listening On http://localhost:${5013}`))
