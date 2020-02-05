# A Deeply Silly Idea: Predicting Possession Outcomes for NFL Games

## Introduction

I thought it'd be neat to calculate the probability of different outcomes at the beginning of a possession for an NFL team.

## The Data

The data used for this analysis comes from two Kaggle datasets (found (here - link) and (here - link)). The first dataset is every play in the NFL from 2009 to 2019. It contains ~450k plays with 255 different features. The second dataset contains historical information about NFL games all the way back to 1966. It has some ~12,500 games with 17 features detailing the games. From both datasets, the most important features for this analysis are the ones we can know before the start of a possession.

- Game Situation - Distance to the end zone, score, time left in the game, possessing team is home team, etc.
- Team v Opponent - Relative strength, expected points in game, leading or trailing, possessing team is favorite, etc.

For the most part the game situation data is from the plays dataset and the team v opponent data is from the historical gambling set.

To reduce data leakage, I used the 2009 - 2017 seasons as my training data and the 2018 season as my hold-out data for validation.

## EDA

For the start of possession analysis

## Predicting Outcomes

Our baseline for a prediction model is to predict that every possession would result in a punt, which occurs 40.8% of the time (in our training data).

# OOPS, I DID IT AGAIN.....
Pie Chart of outcomes in the data

### Logistic Regression

Able to achieve 50.5% accuracy. Describe the model. Find some charts that go with LogReg.

### Naive Bayes

### MLP

### Random Forest 

## Conclusions

## Future Work