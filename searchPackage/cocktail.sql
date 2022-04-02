SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

DROP TABLE IF EXISTS `cocktail`;
CREATE TABLE IF NOT EXISTS `cocktail` (
  `cocktail_id` int NOT NULL AUTO_INCREMENT,
  `cocktail_name` varchar(30) NOT NULL,
  `cocktail_price` varchar(8) NOT NULL,
  `cocktail_description` varchar(300) NOT NULL,
  `cocktail_recipe` varchar(300) NOT NULL,
  PRIMARY KEY (`cocktail_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `cocktail` (`cocktail_id`,`cocktail_name`,`cocktail_price`, `cocktail_description`,`cocktail_recipe`) VALUES
(1, 'Old Fashioned', '$28', "There may be no better test of a bartender's mettle than ordering an Old Fashioned.", "Put sugar in glass. Cover it with dashes of bitters. Add whiskey and stir until sugar dissolves. Add ice, stir again, and serve. If the barman starts shaking the ingredients or muddling fruit, have your next round at another bar."),
(2,'Margarita', '$21', "Cloyingly sweet margarita mixes have given this drink a bad name. A well-made version is a fresh mix of lime juice and tequila, with a hint of sweetener.", "Includes fresh juice, it should be shaken. Serve over ice in a glass with a salted rim"),
(3, 'Cosmopolitan', '$19', "The cosmo became almost ubiquitous in the '90s thanks to the TV show Sex and the City, but this spin on the martini remains just as tasty today as when Carrie Bradshaw made it famous.", "Build all ingredients in a shaker tine with ice and shake. Strain into a martini glass and garnish with lime wheel or zest."),
(4, 'Negroni', '$29', "A favorite of bartenders all over the world, the Negroni is a simple three-ingredient cocktail.", "Stir ingredients with ice."),
(5, 'Moscow Mule', '$26', "Popular for good reason, the Moscow Mule is one of the most refreshing things to sip on a hot summer day.", "Squeeze lime juice into a Moscow Mule mug. Add two or three ice cubes, pour in the vodka, and fill with cold ginger beer. Stir and serve."),
(6, 'Martini', '$28', "James Bond was wrong—whether you drink it with gin or vodka, stirred is the way to go when ordering a martini.", "Stir ingredients in a mixing glass with ice. Strain into chilled martini glass. Squeeze oil from lemon peel into the glass or garnish with olive."),
(7, 'Mojito', '$26', "Originating in Cuba, this refreshing rum-based sip is filled with mint and lime—a perfect combination for sipping by the pool or beach. ", "Muddle mint into a shaker tin, then add ice and all other ingredients. Shake to chill and strain into a highball glass with ice. Top with club soda if desired and garnish with mint."),
(8, 'Whiskey Sour', '$28', "Perhaps the most refreshing whiskey cocktail, this is an old reliable favorite.","Combine ingredients in a cocktail shaker and shake (bartenders use this 'dry shake' to incorporate the egg white). Add ice and shake again. Strain over ice in a rocks glass."),
(9, 'French 75', '$26', "Created during World War I, the name of this drink was supposedly inspired by the fact that taking a sip of it feels like getting shelled with a French 75mm field gun, a powerful piece of artillery.", "Shake gin, simple syrup, and lemon juice with ice. Strain into a champagne glass. Top with champagne."),
(10, 'Manhattan', '$29', "Created sometime in the mid-1800s, the Manhattan is one of the booziest classic drink recipes.","Stir ingredients in a mixing glass with ice. Strain into chilled martini glass or cocktail coupe."),
(11, 'Spritz', '$28', "Low on alcohol and high on refreshment, the spritz has been a crowd-pleasing favorite aperitivo for more than two centuries.", "Mix all ingredients in a wine glass with ice and gently stir. Garnish with an orange slice."),
(12, 'Gimlet', '$28', "A classic gimlet doesn’t require much and it's equally appropriate for a dinner party or a casual night at home." ,"Shake ingredients with ice and strain into cocktail glass."),
(13, 'Sazerac', '$25', "If you like a drink with some bite, give this classic New Orleans concoction a try.", "Rinse a chilled glass with absinthe and discard the absinthe. Stir the other ingredients in a mixing glass, strain into the chilled glass, and garnish."),
(14, "Pimm's Cup", '$23', "The first official Pimm's bar popped up at the 1971 Wimbledon tournament, and now more than 80,000 pints of the quintessential British summer cocktail are served to spectators every year.", "Pile all the ingredients in a tall glass, mix, and sip."),
(15, 'Vesper', '$27', "This drink is the true tipple of the iconic spy—the recipe first appeared in Ian Fleming's 1953 novel Casino Royale in homage to the Bond girl Vesper Lynd.", "Combine all ingredients in a mixing glass with ice and stir until well chilled. Garnish with a lemon twist."),
(16, 'Mimosa', '$22', "We'd like to salute Frank Meier, the bartender at the Ritz Paris who in 1925 reportedly served the first mimosa, the simplest cocktail ever created", "Combine equal parts of the ingredients in a champagne flute."),
(17, 'Tom Collins', '$24', "The Tom Collins is a classic cocktail that's as easy and delicious to whip up at home as it is at your favorite bar. For a truly traditional version, opt for an Old Tom style gin.", "Build all ingredients in a glass with ice and stir gently to combine. Garnish with a lemon slice and a cherry."),
(18, 'Paloma', '$24', "In Mexico the paloma is just as popular as the classic margarita, and with a thirst-quenching combination of tequila, lime, and grapefruit soda it's bound to become a summer favorite of yours too.", "Add tequila and lime to a salt-rimmed glass filled with ice. Top with grapefruit soda."),
(19, 'Sidecar', '$28', "This simple mix of brandy, lemon juice, and orange liqueur dates to the 1920s. Once you try one you'll understand why the recipe has survived so long.", "Shake ingredients with ice. Strain into a rocks glass or a cocktail class with a sugar-coated rim."),
(20, 'Mint Julep', '$25', "The official drink of the Kentucky Derby is worth ordering even when you're not at Churchill Downs.", "Muddle the mint leaves and simple syrup in a mint julep cup. Add bourbon and fill with with crushed ice. Stir until the cup is frosted. Fill with more crushed ice. Serve with a straw and a mint sprig garnish."),
(21, 'Daiquiri', '$22', "Forget the sweet frozen version made with a blender. A classic daiquiri is one of the most well-balanced cocktails around.", "Shake ingredients with ice and strain into cocktail glass. Garnish with lime wheel."),
(22, 'Dark & Stormy', '$18', "The Dark 'n Stormy was created on Bermuda in the late 1800s when British sailors, already rum fans, took to brewing ginger beer and combined their two favorites into one tasty concoction.", "Fill a highball glass with ice and add rum and ginger beer. Garnish with lime."),
(23, 'Martinez', '$20', "Not quite a Manhattan and not quite a Martini, the Martinez uses 'Old Tom', a slightly sweeter style of gin that debuted in the mid-1800s.", "Stir ingredients in a mixing glass with ice. Strain into chilled martini glass or cocktail coupe."),
(24, 'Singapore Sling', '$30', "First crafted at the Long Bar in the Raffles Hotel in Singapore in the early 1900s, the Singapore Sling is known for its bright pink hue and foamy fruit punch cap.", "Combine all liquer and bitters in a cocktail shaker filled with ice. Cover and shake vigorously until thoroughly chilled. Serve in highball glass, toppped with club soda and garnish.");


DROP TABLE IF EXISTS `cocktail_ingredients`;
CREATE TABLE IF NOT EXISTS `cocktail_ingredients` (
  `c_ingredients_id` int NOT NULL AUTO_INCREMENT,
  `cocktail_id` int NOT NULL,
  `c_ingredients` varchar(50) NOT NULL,
  `quantity` varchar(50) NOT NULL,
  PRIMARY KEY (`c_ingredients_id`),
  KEY `FK_cocktail_id` (`cocktail_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `cocktail_ingredients` (`c_ingredients_id`, `cocktail_id`, `c_ingredients`, `quantity`)VALUES
(1, 1, "Bourbon", "2 oz"),
(2, 1, "Angostura Bitters", "2 dashes"),
(3, 1, "Sugar", "1 tablespoon"),
(4, 1, "Orange Peel", "1"),
(5, 2, "Silver Tequila","2 oz"),
(6, 2, "Cointreau", "1 oz"),
(7, 2, "Lime Juice", "1 oz"),
(8, 2, "Salt", "As needed"),
(9, 3, "Citrus Vodka", "1.5 oz"),
(10, 3, "Cointreau", "1 oz"),
(11, 3, "Lime Juice", "0.5 oz"),
(12, 3, "Cranberry Juice", "0.25 oz"),
(13, 4, "Gin", "1 oz"),
(14, 4, "Campari", "1 oz"),
(15, 4, "Sweet Vermouth", "1 oz"),
(16, 5, "Vodka", "2 oz"),
(17, 5, "Ginger Beer", "5 oz"),
(18, 5, "Lime Juice", "0.5 oz"),
(19, 6, "Gin", "3 oz"),
(20, 6, "Dry Vermouth", "0.5 oz"),
(21, 6, "Lemon peel", "1 thin slice"),
(22, 6, "Mint Leaves", "3"),
(23, 7, "White Rum", "2 oz"),
(24, 7, "Lime Juice", "0.75 oz"),
(25, 7, "Simple Syrup", "0.5 oz"),
(26, 8, "Whiskey", "2 oz"),
(27, 8, "Lemon Juice", "1 oz"),
(28, 8, "Sugar", "1 teaspoon"),
(29, 8, "Egg White", "1"),
(30, 9, "Gin", "2 oz"),
(31, 9, "Simple Syrup", "2 dashes"),
(32, 9, "Lemon Juice", "0.5 oz"),
(33, 9, "Champagne", "To Top"),
(34, 10, "Rye Whiskey", "0.5 oz"),
(35, 10, "Sweet Vermouth", "0.5 oz"),
(36, 10, "Angostura Bitters", "0.5 oz"),
(37, 11, "Aperol", "Equal parts"),
(38, 11, "Cinzano Prosecco", "Equal parts"),
(39, 11, "Soda", "1 dash"),
(40, 12, "Gin", "2 oz"),
(41, 12, "Simple syrup", "0.75 oz"),
(42, 12, "Lime Juice", "0.75 oz"),
(43, 13, "Rye Whiskey", "2 oz"),
(44, 13, "Simple Syrup", "0.5 oz"),
(45, 13, "Peychaud's Bitters", "2 dashes"),
(46, 13, "Absinthe", "To Rinse"),
(47, 14, "Pimm's No.1", "1.75 oz"),
(48, 14, "Lemonda", "5 oz"),
(49, 14, "Mint", "As needed"),
(50, 14, "Orange", "As needed"),
(51, 14, "Strawberries", "As needed"),
(52, 14, "Cucumber", "As needed"),
(53, 15, "Gin", "3 oz"),
(54, 15, "Vodka", "1 oz"),
(55, 15, "Lillet Blanc", "0.5 oz"),
(56, 16, "Champagne", "2.5 oz"),
(57, 16, "Orange Juice", "2.5 oz"),
(58, 17, "Old Tom Gin", "2 oz"),
(59, 17, "Simple Syrup", "0.5 oz"),
(60, 17, "Lemon Juice", "1 oz"),
(61, 17, "Club Soda", "To Top"),
(62, 18, "Tequila", "2 oz"),
(63, 18, "Lime Juice", "0.5 oz"),
(64, 18, "Grapefruit Soda", "To Top"),
(65, 19, "VSOP Cognac", "2 oz"),
(66, 19, "Cointreau", "1 oz"),
(67, 19, "Lemon Juice", "0.75 oz"),
(68, 20, "Bourbon", "2 oz"),
(69, 20, "Simple Syrup", "0.25 oz"),
(70, 20, "Mint Leaves", "8-10 pieces"),
(71, 21, "Light Rum", "2 oz"),
(72, 21, "Simple Syrup", "1 oz"),
(73, 21, "Lime Juice", "1 oz"),
(74, 22, "Gosling’s Black Seal Rum", "1.5 oz"),
(75, 22, "Ginger Beer", "To Top"),
(76, 22, "Lime", "1 thin slice"),
(77, 23, "Old Tom Gin", "1.5 oz"),
(78, 23, "Sweet Vermouth", "1.5 oz"),
(79, 23, "Luxardo Maraschino Liqueur", "0.25 oz"),
(80, 23, "Angostura Bitters", "2 dashes"),
(81, 24, "Unsweetened Pineapple Juice", "2 tablespoon"),
(82, 24, "Gin", "1.5 tablespoon"),
(83, 24, "Lime Juice", "1 tablespoon"),
(84, 24, "Grand Marnier", "0.25 oz"),
(85, 24, "Heering", "0.25 oz"),
(86, 24, "Bénédictine", "0.25 oz"),
(87, 24, "Peach-vanilla Bitters", "1 dash"),
(88, 24, "Club Soda", "0.25 cup"),
(89, 24, "Orange Slices", "As needed"),
(90, 24, "Maraschino Cherries", "As needed");

ALTER TABLE `cocktail_ingredients`
  ADD CONSTRAINT `FK_cocktail_id` FOREIGN KEY (`cocktail_id`) REFERENCES `cocktail` (`cocktail_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;