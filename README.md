# FAQs
## SURF Project: Algorithmic Portfolio Management on Cryptocurrencies

* What are we going to do in this project?
  * You are going to make money by buying and selling different cryptocurrencies during a short period of time (hopefully a week).
  * Actually, you aren't doing that by hand. Instead, you are going to write a programme automatically doing it for you.

* What is a cryptocurrency?
  * The most famous example of a cryptocurrency is Bitcoin. People also call them virtual money or virtual coins. You can check the proper definition of cryptocurrency on Wikipedia (https://en.wikipedia.org/wiki/Cryptocurrency), but we only care about the availablility and price movement of cryptocurrencies in markets.

* Where are we going to buy and sell these virtual money's?
  * On a US based cryptocurrency exchange called Poloniex.

* Why Poloniex?
  * Simply because it has the biggest daily trading volume, and the biggest number of tradable cryptocurrencies among all public exchanges.
  * Big daily volume means it is popular so that we are sure there will be someone willing to take what we want to sell, and to offer what we want to buy. Big numbers of tradable coins means we can broadly diversify our investment to minimize risk.

* How does our programme control our Poloniex trading account to buy and sell in real time?
  * This is done by Poloniex’s API (Application Programming Interface). It is publicly available on https://poloniex.com/support/api/ . You may also find wrappers in different computer languages for this API on GitHub (a popular source code sharing platform), https://github.com/s4w3d0ff/python-poloniex for example.
  * We also collect historic prices through API as well.

* Connection to Poloniex is slow. How can we handle frequent trading requests from my computer?
  * We are going to use a virtual linux computer on Amazon Web Services (AWS) to run our auto-trading programme.

* Do I have to be an expert in programming to do this project?
  * No. You can learn coding along the way. However, if you have some programming experience, that would helps very much.

* What programming language are we going to use?
  * Preferably Python, since it is the most popular one in both financial computing and machine learning. However, if you have a very strong attachment to a particular language other than Python, you can use that instead, provided you can persuade your teammates to stick with your choice.

* What methods are we going to use to predict the prices of the cryptocurrencies?
  * We are not going to predict the prices (that was what we did in the SURF project last year 2015). Instead, we want to decide when, what, and how much we are are going to buy or sell to guarantee the maximum profit. This is the so-called portfolio management or portfolio choice problem.

* Then what methods are we going to use to make these decisions?
  * It is up to you and your teammates, but I will provide a list of methods for you to pick up. 
  * However, preferably, I would like you to try out some modern deep learning methods, like Convolutional Neural Network and Recurrent Neural Network.

* Do I have to be familiar with finance to do the project?
  * No. As mentioned in the item above, our methods are mainly from Machine Learning, and it is more to do with Mathematics and Computer Algorithm than Finance. However, financial knowledge does help you understanding the problem setting better, and may provide addition insight to our methods.

* Machine Learning seems to be a difficult topic. Do I have to learn something about it before I do the project?
  * As well as for programming, you can learn Machine Learning by doing the project. However, if you want to prepare yourself better before the start of the project, you can have a look at this free ebook: http://neuralnetworksanddeeplearning.com/
  * We are going to use a Python library call TensorFlow. It make Machine Learning easier. They have some tutorials to start with: https://www.tensorflow.org/

* What are your criteria in choosing student for the project?
  * Your interest in project will be my top consideration. I can tell whether you are really interested by having a small conversation with you.
  * You must be a quick learner who is also willing to learn new things. I can see if you are a quick learner by looking at your academic records.
  * If you have learnt an object-oriented programming language and/or have some programming projects before, it would be a plus. You can show me your previous codes to convince me. However, this is not a requirement.

## Further Questions
If you have further questions, you can come to my office at FB234, and we can discuss them in person, or visit project home at:
![Project Home](images/qrcode_small.jpeg)

Dr Jinjun Liang

Department of Mathematical Sciences

Apr 14 2016


