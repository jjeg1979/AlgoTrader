# **Algo Trader**

The purpose of this document is to follow up a documented and auditable approach towards application design and implementation. This is based on Arjan's guide "Software Design Document Template" that can be found on arjancodes.com/designguide. This document is based on that and follows the same parts detailed in it.

---

## **1. About**
AlgoTrader is aimed at being the tool for algorithmic traders. It tries to cut unnecessary processing times and allows the trader to focus on R&D tasks, by automating most of the mechanical steps that a trader must accomplish in order to start operating one portfolio.
By buying BTTokens (more on this later) the user will be able to unlock most or all of the app features.
The main features AlgoTrader comprises are:

    1. Reading and parsing any html statement from an account or backtesting platform:
      - Genbox (at present time, compatible with MetaTrader 4 platform)
      - MT4/MT5
      - Broker's statement
    After reading it, access to all the operations and relevant information will be avaiable. This is the basics for the rest of the tools that this package will provide.
    2. Obtain the main metrics for the backtest in a consistent manner. In this way, it is possible to combine and/or compare backtests coming from different sources.    
    3. Qualify, according to some specific criteria, if a backtest is "valid" for putting into production. For the first version (MVP) the criteria is fixed as per ITS School recommendations:
       1. k-ratio > 0.2
       2. rf > 9 - 10
       3. Num. ops > 250
       4. Max. exposure <= 0.2
       5. Closing days >= 100    
    4. Store the results in a database to keep a record of the backtests that were analyzed.    
    5. Export the results to .CSV format.    
    6. Portfolio building. Combine backtest using some techniques (ML/AI, Markowitz...)    
    7. Export any combination of backtest in HTML format, similar to the ones provided by other platforms.    
    8. Export metratrader profile for ease of use: allows the user to operate the backtest as soon as it is configured. 
   
The application will allow users to register/login/remember losts pass... and there will be three main groups, according to the Registration CODE used for the registration.
    - VdT: This is a private group that comprises the software creator and his traders sidekicks. These users can see the backtest from all of the users in the same group.
    - ITS: Users coming from ITS School will have a special discount price for every backtest they upload and analyze, portfolio built and some other features.
    - Normal: Users without Registration CODE

---

## **2. User Interface (UI)**
The application will live in a Web Server, so the interface will be a web page. The user will need to register to the website and buy BTTokens to be able to upload/analyze/store backtest results.
After logging in, the user will need to upload a batch of backtest files in HTML format, that the app will parse, analyze and store in the database. A progress bar will indicate the progress, since this process can be very time consuming. 

The user will have access to a web portal where to select the files which will be analyzed. In addition the following information must be provided:
    - Exploration number. It is advisable that every trader keeps a log of the exploration they do. The way a particular user is to decide the convention is out of the scope of this document, but it is recommended that the exploration number changes anytime the symbol, timeframe or internal specification parameters for the backtest creation are changed.
    - Optimization number. Every exploration may have different optimizations done with different algorithms or in different times (for genetic algorithms this is usually the case). 
    - Starting date of the exploration.
    - End date of the exploration.
  
Once the backtests have been analyzed and stored in the database, the user is presented with the main results. The metrics used to validate the backtest will be displayed. In addition, some other metrics will be displayed, for completeness sake:
    - Name of the backtest
    - Symbol for the backtest
    - TimeFrame of the backtest
    - Type of operations: Buy/Sell or Both.
    - Percentage of winning operations over the total.
    - Ratio between the Avg. Winning Operation and the Avg. Losing operation
    - Stagnation period.

The user will only have access to the backtests he/she has analyzed, with the **exception already commented previously** in this document. There will be an option, after the process of the backtests, to download the results as a CSV file, in case the user wants to keep a local copy. The user will be given some useful graphs that will summarize the set of backtests that are owned in the database.
These graphs (doughnout type) will be:
    - Backtests that are valid over the total.
    - Distribution of symbols for all the backtests.
    - ...
  
  ---

  ## **3. Technical Specification**
  This software uses Python/Django/HTML/CSS/JS along with some other libraries (celery,...) SOLID principles should be followed in order to ensure a good integration, quality of code and scalability of the solution. Concurrent programming would also be needed in order to make the app efficient. UML drawings are avaiable as complimentary material to this Markdown document.

  The application should be able to handle error such as Connection Network failures. In case the network presents some issues while the user is uploading/analyzing the files, the app should be able to store the already designed backtests into the database and resume later. The app should remember that a particular backtest is not to be loaded more than once into the database. Backtests shall be uniquely identired by the combination of the following fields:
    - User that uploads the backtest
    - Name of the backtest
    - Exploration number
    - Optimization number
  
  --- 

  ## **4. Testing and security**
   Unit and function tests for all the classes shall be provided using pytest (pytest_django)

   ---

   ## **5. Deployment**
   Heroku will be the platform. Docker will be considered also.

   ---

   ## **6. Planning**
   ---

   ## **7. Broader Context**


   ---
