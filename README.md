# Toxicity Detection Discord Bot
This program is a discord bot that detects toxic behaviour and alerts it to the server.
The final product uses the XGBoost, an optimized gradient boosting algorithm.

## Set Up
###1. Install Requirements
Python 3.5 or higher is needed to run the bot

Run `pip install discord.py`

###2. Create an Application
* Visit the [Discord website](https://discord.com/developers/applications) and click "New Application". 
Make sure you are signed into the Discord website.

* Select a name for your bot when prompted

* Click the "Bot" tab on the left, then click "Add Bot"

* Under Token, click "Copy" and paste it into the token.txt file. 

**Warning: Tokens should never be given to anyone unless trusted. If token is accidentally shared, click "Regenerate"**

###3. Launch the Bot
Run the following:

`python bot.py`

## Algorithm Performances
Before selecting the XGB algorithm, I tested a few algorithms to see which is the best for the job.

### Gaussian Naive Bayes
The Naive Bayes model was by far the worst of the bunch.
The performance score rounded to 89% accuracy, which may seem high at first.
The data I used had a great imbalance, which this algorithm is very sensitive towards.
After calculating the confusion matrix, the false negative rate was at 68%.
This means that the model is predicting messages to be not toxic while they are toxic 68% of the time.

### Weighted Support Vector Machine
The SVM algorithm can be weighted for class imbalances, which helped in giving better results than the previous algorithm.
The over all accuracy of the model trained was 96%, much better than the Naive Bayes model.
The False negative rate was also only 27% now.
The class imbalance seemed to not have as much of an effect on this algorithm.

### XGBoost
After tuning the XGB model as much as possible, I was able to get a score of 94% in accuracy.
The overall accuracy was- although not significantly- worse than the SVM model.
The reason I settled for the XGB model was because the false negative rate was only 18.5%.
The reason why the overall accuracy was lower in the XGB model was because of the false positive rate (predicting something is toxic when it is not).
The XGB model had a false positive rate of 6% while the SVM had a rate of 1%, but this rate is less important than the false engative rate.
