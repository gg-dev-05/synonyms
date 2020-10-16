<h2><b> Synony </b></h2>


This API is hosted on heroku [here](https://synony.herokuapp.com/).

To use this API send a json object to [/app](https://synony.herokuapp.com/app) endpoint (can only be accessed by <b>POST</b> request).  
  Ex. {
        "word" : "ENTER YOUR WORD",
      }
      
      
The API will return the synonym of the given word if it exists and store the word in a database hosted on heroku.

Request :  

![inputJson](https://user-images.githubusercontent.com/59741135/91335033-75edb700-e7ed-11ea-8446-709193705ee9.png)


Response:  
![outputJson](https://user-images.githubusercontent.com/59741135/91335046-7be39800-e7ed-11ea-933c-22a87d734f0a.png)
