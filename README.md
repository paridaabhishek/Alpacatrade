# Alpacatrade
This repository is in the POC state . The main target is to create a BOT which will trade and generate a good amount of return which I will use to give back to the society . The target to productionize the process is by end of 2022.If anyone wants to join hands, very welcome. Also anyone can use my code for a good purpose.

Target achived till now.

1.Tested all the alpeca functionality .
2.Created an small app which will do auto trading with a basic business rule.


Pending Things :
1. Testing more and more business rules.
2. Do a lot of back testting.
3. Create the pod version of the applciation.
4. Scale up the app in cloud .
5. Generate a lot of revenue.
6. Use that for a good cause.

02/20/2022:
1. Created 2 directory strectures . One for all the poc and is research. here all the adhoc codes are stored . The other one user_selected_assets is the actual code. As of now I am able to get the stream data from all the interested stoks and crypto in a proper way with all thread open and close logic. By end of this month the 9-21 EMA 5 mins logic is planned to move to run live on the paper money. By that time also we will have the basic data collection for sunya api will be ready.

02/23/2022:
1. The data collection part with 1 5 15 mins bars with H L O C and with 9 and 21 EMA is comoplete . Seems all the logics to start , stop , archive to be working fine . Initail data testing for O C H L also matching with trading view for all 1 5 15 min bars . Little more testing needed though . The EMA needs a little more analysis as sometime its not maching for 5 15 mins bars .May be the formula needs to be updated.

02/26/2022:

1.The Transaction logic for 921 5 min added and the code is ready for crypto. Next is to code for the same for the stock and run the entire process. The goal is to run the 1st version of the code with paper money with most of the features attched.

03/12/2022:

1.Tested the crypto process end-to-end . Its running fine without any failuers for long hours (itested it running for around 12 hours).Will carry out more stress testing. 


2.On the data validation front the closed price for cryptos are not matching for some websockets and need to be tested further.Mostly its the closed price of the 1 min bar as sometime the socket is pumping multiple records for the same time stamp. 


3.The 9 EMA and 21 EMA also not matching while calucating with closed price for 1,5,15 mins and while compared to trading view.Will test further to make it same with trading view.

