-- MySQL dump 10.13  Distrib 8.4.7, for Win64 (x86_64)
--
-- Host: localhost    Database: maplewood_db
-- ------------------------------------------------------
-- Server version	8.4.7

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `applications`
--

DROP TABLE IF EXISTS `applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `experience` text COLLATE utf8mb4_unicode_ci,
  `location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `position` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `resume_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `submitted_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications`
--

LOCK TABLES `applications` WRITE;
/*!40000 ALTER TABLE `applications` DISABLE KEYS */;
INSERT INTO `applications` VALUES (1,'Sanjay','Rathod','6352920978','sanjayconfido@gmail.com','10 years','Mossbluff','Cashier/Server, Kitchen, Ice Cream, Any Open Position','1772790533_Sanjay_Rathod_Senior_PHP_Developer.pdf','2026-03-06 09:48:53'),(2,'Sanjay','Rathod','6352920978','sanjayconfido@gmail.com','10+ years','Lake Charles, Mossbluff','Kitchen, Sign Holder, Ice Cream','1772790803_Sanjay_Rathod_Senior_PHP_Developer.pdf','2026-03-06 09:53:23');
/*!40000 ALTER TABLE `applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mpl_grp_google_place`
--

DROP TABLE IF EXISTS `mpl_grp_google_place`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mpl_grp_google_place` (
  `id` bigint unsigned NOT NULL DEFAULT '0',
  `place_id` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `rating` double DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `map_url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `website` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `review_count` int DEFAULT NULL,
  `updated` bigint DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mpl_grp_google_place`
--

LOCK TABLES `mpl_grp_google_place` WRITE;
/*!40000 ALTER TABLE `mpl_grp_google_place` DISABLE KEYS */;
INSERT INTO `mpl_grp_google_place` VALUES (1,'ChIJ-SxXbvCFO4YRkHf7kG58nY0','Maplewood Burgers Moss Bluff','https://lh3.googleusercontent.com/place-photos/AEkURDzwiCFxFrvtrPoTEgDELQoRUJrUPyRSQX-dm1bpEBS0rFLaoe7mCFXyaiFb2yCEPcfMWiRfQi2bb4d9IaS36PUuvZhcMYsfvWJ9u38V_WmJ_hqDzkMq7Pvs9Xeoz-H-hi3PAS_pvIVpm6PyYg=s4800-w300-h300','https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet','1355 Sam Houston Jones Pkwy Suite 115, Moss Bluff, LA 70611, USA',4.8,'https://maps.google.com/?cid=10204449145012058000&g_mp=CiVnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLkdldFBsYWNlEAIYBCAA',NULL,'https://www.maplewoodburgers.com/locations/moss-bluff/',585,1765864617117),(2,'ChIJ5diYob6OO4YRLT4hhH-CsBQ','Maplewood Burgers Sulphur','https://lh3.googleusercontent.com/place-photos/AEkURDycYSzdRhxN2guxnbsnCbwVaEYJZATb9CWBahTaUYTHlSNcZ87r-eAbqyEj7HXfGjlIr_qL3iQOyQtplucXkt0y2uAodc_9gPOOH0MsCbCMjqr0MTGZnCVnZshsKd9f7Gb8qxx3431SCwuA=s4800-w300-h300','https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet','4124 Maplewood Dr, Sulphur, LA 70663, USA',4.9,'https://maps.google.com/?cid=1490834960848862765&g_mp=CiVnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLkdldFBsYWNlEAIYBCAA',NULL,'https://www.maplewoodburgers.com/locations/sulphur/',1565,1765966062459),(3,'ChIJ5cfEy7qHO4YRzq6zw6Yeu8k','Maplewood Burgers Lake Charles','https://lh3.googleusercontent.com/places/ANXAkqGpFUFH5SK8nD8Gftsjfuu3_FR0QmvJ-9JGRAkt8QjmqTKjDTvgqq4ainq3y4SHIjBgUKn3Th8ZxpMhVjwpTfvuVvVD9xh1Sw=s4800-w300-h300','https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet','4453 Nelson Rd, Lake Charles, LA 70605, USA',4.7,'https://maps.google.com/?cid=14536245923865145038&g_mp=CiVnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLkdldFBsYWNlEAIYBCAA',NULL,'https://www.maplewoodburgers.com/locations/lake-charles/',1233,1765865350194);
/*!40000 ALTER TABLE `mpl_grp_google_place` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mpl_grp_google_review`
--

DROP TABLE IF EXISTS `mpl_grp_google_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mpl_grp_google_review` (
  `id` bigint unsigned NOT NULL DEFAULT '0',
  `google_place_id` bigint unsigned NOT NULL,
  `rating` int NOT NULL,
  `text` varchar(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `time` int NOT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `language` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `author_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `author_url` varchar(127) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `profile_photo_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `provider` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `images` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci,
  `reply` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci,
  `reply_time` int DEFAULT NULL,
  `hide` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT ''
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mpl_grp_google_review`
--

LOCK TABLES `mpl_grp_google_review` WRITE;
/*!40000 ALTER TABLE `mpl_grp_google_review` DISABLE KEYS */;
INSERT INTO `mpl_grp_google_review` VALUES (1,1,5,'',1765758040,NULL,NULL,'Sarah StCyr','https://www.google.com/maps/contrib/101287172447230186694/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ-SxXbvCFO4YRkHf7kG58nY0_61accd7485e75ff76cbfd070ef6798fa.jpg',NULL,NULL,NULL,NULL,''),(2,1,5,'Great service, great food Reba was a great waitress!!!',1765738839,NULL,'en','Mandi Mills','https://www.google.com/maps/contrib/103876541848058906819/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ-SxXbvCFO4YRkHf7kG58nY0_1767ab9c2669f576a999bd5f7f2bc1b2.jpg',NULL,NULL,NULL,NULL,''),(3,1,5,'Really good burger, but make sure you save room for the Ice-cream. Service was wonderful, we will be back',1765670095,NULL,'en','Jeff Weldele','https://www.google.com/maps/contrib/109492086683337159839/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ-SxXbvCFO4YRkHf7kG58nY0_7e20ec0ff6573594a1e0cb12dff09264.jpg',NULL,NULL,NULL,NULL,''),(4,1,5,'Christie and Reba took great care of us and thr burgers were delicious.',1765670084,NULL,'en','Marjie Weldele','https://www.google.com/maps/contrib/109915219810305087223/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ-SxXbvCFO4YRkHf7kG58nY0_42bc5a47ebe8f88dc84178096e955a41.jpg',NULL,NULL,NULL,NULL,''),(5,1,5,'',1765557009,NULL,NULL,'Bonnie Saucier','https://www.google.com/maps/contrib/112443714858900583268/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ-SxXbvCFO4YRkHf7kG58nY0_b2cbb5be0e31dcaebb068e0db8c499cd.jpg',NULL,NULL,NULL,NULL,''),(6,1,5,'The food was amazing! Service was great! Thanks Christy! Ice cream goes with breakfast tooΓÇª.just incase you didnΓÇÖt know!',1760887260,NULL,'en','Jill Elfert','https://www.google.com/maps/contrib/116525014127618691479/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ-SxXbvCFO4YRkHf7kG58nY0_5a5ba17ae5df9bfb3341e4325e14724c.jpg',NULL,NULL,NULL,NULL,''),(7,1,5,'Definitely plan on visiting again.  Great burgers at a good price.  Christy was our server and she was fantastic.',1761854034,NULL,'en','Christine Gruber','https://www.google.com/maps/contrib/115407742395795522319/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ-SxXbvCFO4YRkHf7kG58nY0_82376c4036daa8c1b69f2bef795c1ac7.jpg',NULL,NULL,NULL,NULL,''),(8,1,4,'The food and service is amazing. The meat is tender, the shakes are amazing. Best shakes IΓÇÖve had in forever. ItΓÇÖs not a place you want to sit in if you have any hearing left.\n\nThe ringing from the TVs makes my brain vibrate. 60db of pure manufactured tinnitus. It could be a torture mechanism. ItΓÇÖs been like that for months. They have 11 televisions on mute that do nothing but angrily scream at you the sound of its horrible species.\n\nIΓÇÖd rather stare at the wall and no TV. IΓÇÖd rather miss all the games.\n\nHowever, I can just order to-go. I just figured the issue would be fixed by now (itΓÇÖs been months since I decided to eat in) but idk what they can do to fix it.\n\nTo be fair, if I HAD to eat in and be subjected to 90 of the Phillips TVs and couldnΓÇÖt get to-go, IΓÇÖd just have to deal with it because the food is amazing.',1763324947,NULL,'en','OPC Development','https://www.google.com/maps/contrib/109179151469917034070/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ-SxXbvCFO4YRkHf7kG58nY0_332559a1b425b74e7870ba160e836cca.jpg',NULL,NULL,NULL,NULL,''),(9,1,5,'First time and had the Monday special. 1/4 pound burger with fries. Added queso to the fries! A lot of bread for the burger but the flavor was great and fires were really good!!',1759767143,NULL,'en','Ginger Menard','https://www.google.com/maps/contrib/101173376179141716493/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ-SxXbvCFO4YRkHf7kG58nY0_ba79068aaa9f3ab00639eefa0370bdb7.jpg',NULL,NULL,NULL,NULL,''),(10,1,5,'1st time here at Maplewood Burgers-Moss Bluff, La! The sweet potato fries were so amazing & fresh! My husband ate the stuffed shrimp burger and said it was great!! WeΓÇÖll be back!',1758589383,NULL,'en','Christy Stelly','https://www.google.com/maps/contrib/114689152094313734664/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ-SxXbvCFO4YRkHf7kG58nY0_2408da9ed0989fb0505e1e3322759a7a.jpg',NULL,NULL,NULL,NULL,''),(11,2,5,'Good food and good service! Maria took my order and served me with a smile and was happy to serve me.',1765807013,NULL,'en','Bridget Parker','https://www.google.com/maps/contrib/100041059853477995714/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5diYob6OO4YRLT4hhH-CsBQ_c3e13040bfba5e3079834fd69c1470df.jpg',NULL,NULL,NULL,NULL,''),(12,2,5,'IΓÇÖve been trying there stuffed burgers and they are amazing with the best shakes IΓÇÖve probably ever had with great services by Marini',1765753015,NULL,'en','Trystan Bankston','https://www.google.com/maps/contrib/106645346130975461696/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5diYob6OO4YRLT4hhH-CsBQ_38341892ebc43b7305fcad14e4b64f9b.jpg',NULL,NULL,NULL,NULL,''),(13,2,5,'Food here is amazing and Marini is the  best amazing service to go with it',1765753001,NULL,'en','Leeann bankston','https://www.google.com/maps/contrib/116506931188478876417/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5diYob6OO4YRLT4hhH-CsBQ_28ce4d9a3fa6d569c7cfc6cdc4efef54.jpg',NULL,NULL,NULL,NULL,''),(14,2,5,'',1765752855,NULL,NULL,'Austin Bankston','https://www.google.com/maps/contrib/101114085203454188003/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5diYob6OO4YRLT4hhH-CsBQ_d1775079119850d38d403451a8f8473c.jpg',NULL,NULL,NULL,NULL,''),(15,2,5,'food is great and this milkshake is bomb',1765748651,NULL,'en','Hugh hyatt','https://www.google.com/maps/contrib/104770125566442538116/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5diYob6OO4YRLT4hhH-CsBQ_146db8a97d3f5460fb1aa667a16edb7f.jpg',NULL,NULL,NULL,NULL,''),(16,2,5,'The food here was soo good. We were helped by Marina and Lorraine, they were both so helpful and super sweet. We shared Bacon attack burger, and subbed our side of fries for loaded Philly cheesesteak fries, and brisket loaded fries. Everything was soo amazing. 10/10 would recommend. WeΓÇÖll definitely be back!',1765161105,NULL,'en','Nancy Le','https://www.google.com/maps/contrib/109004298790934309990/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5diYob6OO4YRLT4hhH-CsBQ_d69a547173bb9b0d6303ac24fe36aa1d.jpg',NULL,NULL,NULL,NULL,''),(17,2,5,'The hostess was incredibly friendly, attentive, and helpful! My boyfriend and I were looking for a good spot to eat, and weΓÇÖre so glad we ended up here. We arrived around 5 PM and immediately loved the warm, comforting atmosphere.\n\nNow the foodΓÇöamazing. We ordered the Cajun Kick Burger and the El Bruno Stuffed Burger, and both were absolutely delicious. Perfectly seasoned, juicy, and bursting with flavorΓÇösome of the best burgers IΓÇÖve ever had. We also treated ourselves to the Oreo Attack shake, which was rich, creamy, and the perfect sweet ending to the meal.\n\nWeΓÇÖll definitely be back!',1752968208,NULL,'en','Adrianna','https://www.google.com/maps/contrib/116616016349568255340/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5diYob6OO4YRLT4hhH-CsBQ_ca4026e1ace02e11bf025be2e024722f.jpg',NULL,NULL,NULL,NULL,''),(18,2,5,'This place is definitely worth the stop and we will be back!!! I got the Cajun kick stuffed burger and Honestly might have been the best burger I have ever had!! I wish I could have ordered a sample patter to try them all. Mrs Maria we canΓÇÖt thank you enough for the hospitality and the recommendations and we hope to see yall again soon!',1764816047,NULL,'en','Mitchell Mulkey','https://www.google.com/maps/contrib/104327666252071573570/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5diYob6OO4YRLT4hhH-CsBQ_ba994b1e23bb1735ac934290380f9888.jpg',NULL,NULL,NULL,NULL,''),(19,2,5,'If youΓÇÖve ever wondered what culinary magic looks like when it hides out in a convenience store, Maplewood Burgers is your answer. Tucked between shelves of energy drinks and last-minute snacks is a burger joint that could teach ΓÇ£realΓÇ¥ restaurants a thing or two about greatness.\n\nWe went bigΓÇöconvenience-store-food-but-make-it-gourmet big. The stuffed boudin burger was an absolute masterpiece: smoky, savory, and so good it should come with a warning label for emotional attachment. The onion rings were perfectly crisp, like theyΓÇÖd been preparing for greatness their whole lives, and the chorizo fries? LetΓÇÖs just say they deserve their own national holiday. Even the kidsΓÇÖ chicken nuggets were suspiciously deliciousΓÇölike Maplewood couldnΓÇÖt help but overachieve.\n\nHonestly, it might be one of the best burgers IΓÇÖve ever had, and the customer service was fantastic!  Maplewood Burgers is proof that sometimes the finest dining happens where you least expect itΓÇöright between the cold drinks and the scratch-offs.',1763774818,NULL,'en','Mark Wilson','https://www.google.com/maps/contrib/116928649012670290011/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5diYob6OO4YRLT4hhH-CsBQ_f38011f1cda4aac1f35005ab78506a33.jpg',NULL,NULL,NULL,NULL,''),(20,2,5,'Best burgers and milkshakes of your life! Marini is the burger queen ≡ƒææ Super helpful and sweet. We will be back for the stuffed patties and breakfast next. WeΓÇÖre so happy we got to visit the OG locationΓÇö Thank you for making our date night fun!',1761698243,NULL,'en','Jeslyn Branick Hebert','https://www.google.com/maps/contrib/111121704041952304378/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5diYob6OO4YRLT4hhH-CsBQ_e695c385e33950970419a0e660f4dbf7.jpg',NULL,NULL,NULL,NULL,''),(21,3,5,'Miceala was a very nice server and gave us very great recommendations!',1765825205,NULL,'en','Kayla','https://www.google.com/maps/contrib/117151585271340059665/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5cfEy7qHO4YRzq6zw6Yeu8k_abcaf34d0b732c174428910822f47f06.jpg',NULL,NULL,NULL,NULL,''),(22,3,5,'Everything was excellent and Reba provided superb service!',1765761168,NULL,'en','Michael Lee','https://www.google.com/maps/contrib/103986362771221409999/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5cfEy7qHO4YRzq6zw6Yeu8k_db716cd673b33478c2f83f6d2f35f988.jpg',NULL,NULL,NULL,NULL,''),(23,3,5,'Lawanna and Reba were amazing and so sweet! Definitely coming back!!!',1765154529,NULL,'en','Katelyn','https://www.google.com/maps/contrib/106844118700572272299/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5cfEy7qHO4YRzq6zw6Yeu8k_efb07991a9e90f34432035f03c198e59.jpg',NULL,NULL,NULL,NULL,''),(24,3,5,'Reba & Luwanna customer service was amazing! Food was outstanding!',1765146824,NULL,'en','Anita Barker','https://www.google.com/maps/contrib/103640566638619957805/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5cfEy7qHO4YRzq6zw6Yeu8k_901c5212f479038ed5b43684a86bb3a4.jpg',NULL,NULL,NULL,NULL,''),(25,3,5,'Reba was awesome and the food was really good! Great deals on the app and the milkshake was glorious.',1765144908,NULL,'en','Ben McF','https://www.google.com/maps/contrib/109710067133884588117/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5cfEy7qHO4YRzq6zw6Yeu8k_d576804eca2f824af8956c195fe0978f.jpg',NULL,NULL,NULL,NULL,''),(26,3,4,'What to say about Maplewood burgers in Lake Charles first and foremost Reba, your customer service was excellent and thank you. Second the tots were delicious and  the onion rings were so good they barely made it to the house!  Third, can you see that cheese pull? Finally, the taste, I had the Mushroom Swiss burger and I would give it a strong 8 out of 10.  The burger itself lacked flavor. If I was a person that didn\'t like too many toppings and condiments I probably be disappointed by the lack of seasoning',1764117604,NULL,'en','Donald Buckner','https://www.google.com/maps/contrib/113591968837481667249/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5cfEy7qHO4YRzq6zw6Yeu8k_e4598bf5107852e66d714c03888069e0.jpg',NULL,NULL,NULL,NULL,''),(27,3,5,'We are from San Antonio, Texas driving through for an event.  I am always looking for the best burger in town and Maplewood did not disappoint.  My family and I tried 3 different burgers todayΓÇªamazing, juicy, flavorful, and unique burgersΓÇªI would drive out of my way to come here again.  The sweet potatoes fries were on point, trulyΓÇªthe best IΓÇÖve had!  My husband said the onion rings were the best heΓÇÖd ever had!  Thank you, Madison, for an amazing experience!  Y\'all are the best!!',1754083527,NULL,'en','Dawn Ballesteros','https://www.google.com/maps/contrib/108697445305324861110/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5cfEy7qHO4YRzq6zw6Yeu8k_b21369c5195c8ef8f9b74c35aba2df07.jpg',NULL,NULL,NULL,NULL,''),(28,3,5,'This was the Best burger we have ever had. We had a philly cheese steak stuffed burger, Swiss and mushroom stuffed burger, and a beacon stuffed burger. All was cooked to perfection, super juicy.  Will definitely be back! Highly recommend.',1754856887,NULL,'en','Robin H.','https://www.google.com/maps/contrib/106190157363195806234/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5cfEy7qHO4YRzq6zw6Yeu8k_14a075da1271455efb88b72326bfa62d.jpg',NULL,NULL,NULL,NULL,''),(29,3,5,'Fun atmosphere my family and i enjoyed eatting at this place. Big shout out to our waitress she was awesome!! Reba!! We will be back!≡ƒÆ»',1761051007,NULL,'en','Caylin Simon','https://www.google.com/maps/contrib/117920505181016888076/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5cfEy7qHO4YRzq6zw6Yeu8k_f317a4bbe1218f5bf405448624623cee.jpg',NULL,NULL,NULL,NULL,''),(30,3,5,'This is a very special place. The breakfast was full of flavor. The owner took my order. He was genuinely concerned about my well-being. He cares deeply about his customers. He also cares about the food delivery guys that come in.  This establishment reflects my Father\'s Love.  If you want to sew into a kingdom business, then this is the place!',1753882721,NULL,'en','Kelly Tompkins','https://www.google.com/maps/contrib/116308950304386208135/reviews','http://localhost/maplewoodburgers/wp-content/uploads/ChIJ5cfEy7qHO4YRzq6zw6Yeu8k_c2f0502d3e69f9bbce466aa7559030e8.jpg',NULL,NULL,NULL,NULL,'');
/*!40000 ALTER TABLE `mpl_grp_google_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `setting_key` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `setting_value` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `setting_key` (`setting_key`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES (1,'chat_widget_key','27b4d9ed-5c67-4eb0-afcf-9233da0781a9'),(2,'smtp_host','smtp.gmail.com'),(3,'smtp_port','587'),(4,'smtp_user','sanjayconfido@gmail.com'),(5,'smtp_password','admin123'),(6,'smtp_from_email','sanjayconfido@gmail.com');
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin123');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-06 18:38:37
