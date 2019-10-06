import numpy as np
import Utils_AA as utils
import pandas as pd

#exception introduced to get out from the most nested loops if we have to skip everything and run to next user
class StopLookingForThings(Exception): pass

#Parameters for Base Stations
Dist_of_BS = int(input("Enter the distance: ")) #in kms
BS_dist = Dist_of_BS * 1000
N_Channel_BS = 30 #Each sector has 30 channels
#NOTE: sim_hour to be entered by user
sim_hour = int(input("Enter the simulation hour: "))
#Paramteres for Mobile Station
RSL_Thresh = -102 #dBm
N_of_Users = int(input("Enter the number of Users: ")) # (to be requested by user)
Call_rate = 1 #1 call per hour
Av_Call_Duration = 15 # 3 minutes per call
Mob_Speed = int(input("Enter the speed of the mobile: ")) #m/s (to be requested by user)
HO_Timer = 3 # Time in which Handoff should be completed
SHAD_RES = 10 #in mtrs
Step_Size = 1 # in sec
simulation_time = sim_hour * 3600 #in secs
#prob of call (units in secs)
prob_of_call = (Call_rate * (Step_Size/3600)) 

dist_by_user = Mob_Speed * Step_Size # in mtrs

#Exponential distribution of call durationd to users
init_call_dur = np.random.exponential(180,N_of_Users)
newarr = init_call_dur.round()
User_Call_Duration = list(newarr)

#initiate location of the users
Location_arr = np.random.uniform(0,BS_dist,N_of_Users) #will give the current location of the user
init_loc_arr = Location_arr

#initiate dictionary
User_Data = {}
for i in range(0,N_of_Users):#NOTE TBD
    #0th - is call set up or not
    #1st - location of the user
    #2nd - direction in which the user is moving
    #3rd - Serving Base station
    #4th - HO status to BS
    #5th - HO time counter
    #6th - Call Drop Counter/ (No being used anynmore, have different counter)
    #7th - User Archived or not
    #8th - Handover ongoing or completed status
    User_Data[i] = ['False',Location_arr[i],'Stationary','Null','Null',0,0,'Null','Null']



#print("Initial dict = ",User_Data)
Call_attempt_counter = 0 # Counterr for total number of call attempts at the end of simulation
Succ_call_conn = 0 # Counter for successful call connections at the end of simulation
Succ_complete_call = 0 # Coounter for successful calls completed at the end of simulation
HO_attempt_BS12 = 0 # Counter for HO attempts by BS1 to BS2 at the end of simulation
HO_attempt_BS21  = 0 # Counter for HO attempts by BS2 to BS1 at the end of simulation
HO_Succ_BS12 = 0 # Counter for successful HO by BS1 to BS2 at the end of simulation
HO_Succ_BS21 = 0 # Counter for successful HO by BS2 to BS1 at the end of simulation
HO_Fail_BS12 = 0 # Counter for failed HOs from BS1 to BS2 at the end of simulation
HO_Fail_BS21 = 0 # Counter for failed HOs from BS2 to BS1 at the end of simulation
Call_Block_Cap2 = 0 # Counter for Call blocks on BS1 due to capacity 
Call_Block_Cap1 = 0 # Counter for Call blocks on BS2 due to capacity
Call_Block_Strength1 = 0 # Counter for Call blocks due to low strength of BS1
Call_Block_Strength2 = 0 # Counter for Call blocks due to low strength of BS2

Drop_Call_BS1 = 0 # Counter for dropped calls at BS1
Drop_Call_BS2 = 0 # Counter for dropped calls at BS2

Active_Call_BS_1 = 0 # Counter for Active Calls at BS1 at the end of simulation
Active_Call_BS_2 = 0 # Counter for Active calls at BS2 at the end of simulation
Step_Size = 1 # Step size in secs


RSL_BS_1 = {} # Dictionary to store signal strenght at every 1sec for BS1
RSL_BS_2 = {} # Dictionary to store signal strenght at every 1sec for BS2

#For loop to initialize the RSLs of both the BSs as 0
for index in range(0,N_of_Users):
    RSL_BS_1[index] = 0
    RSL_BS_2[index] = 0

# calc_Shadowing function is used to calculate the shadowing at every 10 mtrs.
# This function will give us total 1200 values and we will select values on the index nearest to the location of the user
def calc_Shadowing(BS_dist):
    random_val = np.random.normal(0, 2, BS_dist)
    return random_val


# calculates and stores the shadow value at evry 10mtrs for BS1
Shadowing_BS_1 = tuple(calc_Shadowing(BS_dist))
# calculates and stores the shadow value at evry 10mtrs for BS2
Shadowing_BS_2 = tuple(calc_Shadowing(BS_dist))

while(Step_Size <= simulation_time): 
    for i in range(0,N_of_Users):#NOTE TBD
        try:
            if(User_Data[i][7] == 'User_Archived'):
                i = i + 1
                raise StopLookingForThings()
            else: 
                if(User_Data[i][0] == 'False'): # For those users who don't have an active call, there probability will be checked 
                    user_prob = np.random.uniform(0,3600) # the probablity will be selected at random between 0 and 3600  
                    if(user_prob >=1): # if user prob is greater than or equal to than 1 then we are done with that user for now, no call will be initiated
                        i = i + 1 # increment for the next user
                        raise StopLookingForThings() # For users whose prob. is greater than or equal to 1, we are done with them for now
                    else:
                        Call_attempt_counter = Call_attempt_counter + 1 # users whose probability is less than 1 call they will try to attempt the call
                        if(User_Data[i][1] >= BS_dist-1 or User_Data[i][1] <= 1): # if the user is at a within 1 mtr of any of BS, we are done with that user for now. Move on to next user
                            User_Data[i][7] = 'User_Archived'
                            User_Data[i][0] = 'False'
                            User_Call_Duration[i] = 0
                            i = i + 1
                            raise StopLookingForThings()
                        else: # For all the other users we will calculate the RSL at every 1 sec from both the Base Stations
                            RSL_BS_1[i] = utils.calc_RSL(User_Data[i][1],Shadowing_BS_1) # Calculating RSL for BS1
                            RSL_BS_2[i] = utils.calc_RSL(BS_dist - User_Data[i][1],Shadowing_BS_2) # Calculating RSL for BS2
                        if(RSL_BS_1[i] > RSL_BS_2[i]):# Comparing RSL of BS1 with BS2
                            if(RSL_BS_1[i] >= RSL_Thresh): # if RSL of BS1 > Threshold
                                if(Active_Call_BS_1 < N_Channel_BS and Active_Call_BS_1 >= 0 ):# Checking whether we have the channels available at BS1 
                                    if(User_Call_Duration[i] > 0 and User_Data[i][1] > 0 and User_Data[i][1] <=(BS_dist-1) ):
                                        User_Call_Duration[i] = User_Call_Duration[i] - 1 # Call duration timer for that user will start decreasing
                                        User_Data[i][1] = User_Data[i][1] + dist_by_user # User will move 15mts ahead of his location (BS1 -> BS2)
                                        User_Data[i][2] = 'East' # Will provide direction in which the user is moving
                                        User_Data[i][3] = 'Serving_BS_1'# Serving BS
                                        Active_Call_BS_1 = Active_Call_BS_1 + 1# Total number of Active Calls at that Base Station will be incremented by 1
                                        Succ_call_conn = Succ_call_conn + 1 # Since call is set up, this counter will be incremented by 1
                                        User_Data[i][0] = 'True' # True means call for that particular user has been set up
                                    else:
                                        User_Data[i][0] = 'False'# False means no call has been setup for that particular user
                                elif(Active_Call_BS_1 >= N_Channel_BS):# if there are no channels available at BS1, all of them are occupied, then call will be dropped because of capacity
                                    Call_Block_Cap1 = Call_Block_Cap1 + 1 #Capacity block counter for BS1 will be incremented by 1
                                    if(RSL_BS_2[i] >= RSL_Thresh): # compares the RSL of BS2 with the Threshold value
                                        if(Active_Call_BS_2 < N_Channel_BS and Active_Call_BS_2 >= 0):#Will check if the BS2 has an Active Channel or not for call establishment
                                            if(User_Call_Duration[i] > 0 and User_Data[i][1] > 0 and User_Data[i][1] <=(BS_dist-1) ):
                                                User_Call_Duration[i] = User_Call_Duration[i] - 1
                                                User_Data[i][0] = 'True' #Call setup marked as 1
                                                User_Data[i][1] = User_Data[i][1] + dist_by_user 
                                                User_Data[i][2] = 'East' #User will continue moving in same direction 
                                                User_Data[i][3] = 'Serving_BS_2' # But serving BS will be BS 2
                                                Active_Call_BS_2 = Active_Call_BS_2 + 1
                                                Succ_call_conn = Succ_call_conn + 1
                                        else:
                                            Drop_Call_BS1 = Drop_Call_BS1 + 1 # Call drop when channels is not available on BS2,
                                            #then Drop call counter for BS1 will be incremented by 1
                                    else:
                                        Drop_Call_BS1 = Drop_Call_BS1 + 1 # Call drop when channels are not available on BS1 
                                        #and strength of BS2 is not enough
                            else:
                                Call_Block_Strength1 = Call_Block_Strength1 + 1
                        elif(RSL_BS_2[i] > RSL_BS_1[i]): # Comparing RSL of BS2 with RSL of BS1
                            if(RSL_BS_2[i] >= RSL_Thresh): # Comparing RSL of BS2 with the RSL threshold
                                if(Active_Call_BS_2 < N_Channel_BS and Active_Call_BS_2 >= 0):# Checking the availabilty of channels at BS2, if all the conditions are met call will be established
                                    if(User_Call_Duration[i] > 0 and User_Data[i][1] > 0 and User_Data[i][1] <=(BS_dist-1) ):
                                        User_Call_Duration[i] = User_Call_Duration[i] - 1
                                        User_Data[i][0] = 'True' #Call setup marked as 1
                                        User_Data[i][1] = User_Data[i][1] - dist_by_user # User will move 15mts ahead of his location (BS2 -> BS1)
                                        User_Data[i][2] = 'West' #Update user's direction
                                        User_Data[i][3] = 'Serving_BS_2' # Serving BS -> 2
                                        Active_Call_BS_2 = Active_Call_BS_2 + 1
                                        Succ_call_conn = Succ_call_conn + 1
                                    else:
                                        User_Data[i][0] = 'False'
                                elif(Active_Call_BS_2 >= N_Channel_BS):  # if there are no channels available at BS2, all of them are occupied, then call will be dropped because of capacity
                                    Call_Block_Cap2 = Call_Block_Cap2 + 1 #Capacity block counter of BS2 will be incremented by 1
                                    if(RSL_BS_1[i] >= RSL_Thresh): # compares the RSL of BS2 with the Threshold value
                                        #Will now check if the BS1 has an Active Channel or not for call establishment
                                        if(Active_Call_BS_1 < N_Channel_BS and Active_Call_BS_1 >= 0):
                                            if(User_Call_Duration[i] > 0 and User_Data[i][1] > 0 and User_Data[i][1] <=(BS_dist-1) ):
                                                User_Call_Duration[i] = User_Call_Duration[i] - 1
                                                User_Data[i][0] = 'True' #Call setup marked as 1
                                                User_Data[i][1] = User_Data[i][1] - dist_by_user #User will be moving in same direction
                                                User_Data[i][2] = 'West' #Therefor it is still west
                                                User_Data[i][3] = 'Serving_BS_1'
                                                Active_Call_BS_1 = Active_Call_BS_1 + 1
                                                Succ_call_conn = Succ_call_conn + 1
                                        else:
                                            Drop_Call_BS2 = Drop_Call_BS2 + 1
                                    else:
                                        Drop_Call_BS2 = Drop_Call_BS2 + 1    
                            else:
                                Call_Block_Strength2 = Call_Block_Strength2 + 1                                               
                elif(User_Data[i][0] == 'True'):
                    # Update users location
                    if(User_Data[i][2] == 'West'):
                        User_Data[i][1] = User_Data[i][1] - dist_by_user
                    elif(User_Data[i][2] == 'East'):
                        User_Data[i][1] = User_Data[i][1] + dist_by_user   
                            
                    #If user has moved past the base stations then free the channel and move on to next user
                    if((User_Data[i][1] >= BS_dist-1  or User_Data[i][1] <= 1) and User_Call_Duration[i] > 0):
                        if(User_Data[i][3] == 'Serving_BS_2' ):
                            Active_Call_BS_2 = Active_Call_BS_2 - 1
                        elif(User_Data[i][3] == 'Serving_BS_1' ):
                            Active_Call_BS_1 = Active_Call_BS_1 - 1
                        User_Data[i][0] = 'False'
                        User_Call_Duration[i] = 0
                        User_Data[i][7] = 'User_Archived'
                        User_Data[i][8] = 'Call_Completed as user moved past the BS_2'
                        Succ_complete_call = Succ_complete_call + 1
                        i = i + 1
                        raise StopLookingForThings()          
                    else:
                        #calculate the RSLs on updated locations
                        RSL_BS_1[i] = utils.calc_RSL(User_Data[i][1],Shadowing_BS_1)
                        RSL_BS_2[i] = utils.calc_RSL(BS_dist - User_Data[i][1],Shadowing_BS_2)
                    if(User_Call_Duration[i] > 0 ): #If user is still on call
                        User_Call_Duration[i] = User_Call_Duration[i] - 1
                         
                        if (User_Data[i][3] == 'Serving_BS_1'):
                            if(RSL_BS_1[i] < RSL_Thresh):
                                #If the serving BS1's strength is not enough
                                if (User_Data[i][8] == 'Handover_Ongoing'): #if this user was in process of HO but couldnt complete
                                    Active_Call_BS_2 = Active_Call_BS_2 - 1 #free the channel of other BS which he was holding for HO
                                    HO_Fail_BS12 = HO_Fail_BS12 + 1 #Failed HO 
                                Drop_Call_BS1 = Drop_Call_BS1 + 1 #Call will get dropped
                                Active_Call_BS_1 = Active_Call_BS_1 - 1 #Free the channel
                                User_Data[i][7] = 'User_Archived'
                                User_Data[i][8] = 'Call dropped due to strength (but not blocked)'
                                User_Data[i][0] == 'False'
                                i = i + 1
                                raise StopLookingForThings()          
                            elif(RSL_BS_1[i] >= RSL_Thresh):
                                if(RSL_BS_2[i] > RSL_BS_1[i]):
                                    if(Active_Call_BS_2 < N_Channel_BS and Active_Call_BS_2 >=0 ):      
                                        while(User_Data[i][5] < HO_Timer):
                                            User_Data[i][8] = 'Handover_Ongoing'
                                            if(User_Data[i][5] == 0):
                                                Active_Call_BS_2 = Active_Call_BS_2 + 1 #Hold the channel of other BS for 3 sec
                                                HO_attempt_BS12 = HO_attempt_BS12 + 1 #Update HO Attempt
                                            User_Data[i][5] = User_Data[i][5] + 1 #Counter of 3 sec for that user as HO takes time
                                            i = i + 1
                                            raise StopLookingForThings()
                                        
                                        #Paramters updated for Succesful HO
                                        User_Data[i][5] = 0   
                                        Active_Call_BS_1 = Active_Call_BS_1 - 1
                                        User_Data[i][4] = 'HO_to_BS_2'
                                        User_Data[i][3] = 'Serving_BS_2'
                                        User_Data[i][8] = 'Handover_Completed'
                                        HO_Succ_BS12 = HO_Succ_BS12 + 1

                                    else:
                                        #Counters for Failed HO
                                        HO_attempt_BS12 = HO_attempt_BS12 + 1 
                                        HO_Fail_BS12 = HO_Fail_BS12 + 1 # HO failed incremeneted as it is failed HO
                                        Call_Block_Cap2 = Call_Block_Cap2 + 1 #Capacity block as channel wasn't available on BS 2 to give HO

                        elif(User_Data[i][3] == 'Serving_BS_2'):
                            #If the serving BS2's strength is not enough
                            if(RSL_BS_2[i] < RSL_Thresh):
                                if (User_Data[i][8] == 'Handover_Ongoing'): #if this user was in process of HO but couldnt complete
                                    Active_Call_BS_1 = Active_Call_BS_1 - 1 #free the channel of other BS which he was holding for HO
                                    HO_Fail_BS21 = HO_Fail_BS21 + 1 #HO Failed
                                Drop_Call_BS2 = Drop_Call_BS2 + 1 # Drop call for BS2
                                Active_Call_BS_2 = Active_Call_BS_2 - 1
                                User_Data[i][7] = 'User_Archived'
                                User_Data[i][8] = 'Call dropped due to strength (but not blocked)'
                                User_Data[i][0] == 'False'
                                i = i + 1
                                raise StopLookingForThings()  
                            elif(RSL_BS_2[i] >= RSL_Thresh):
                                if(RSL_BS_1[i] > RSL_BS_2[i]):
                                    #increase counter for HO
                                    if(Active_Call_BS_1 < N_Channel_BS and Active_Call_BS_1 >=0):
                                        while(User_Data[i][5] < HO_Timer):
                                            User_Data[i][8] = 'Handover_Ongoing'
                                            if(User_Data[i][5] == 0):
                                                Active_Call_BS_1 = Active_Call_BS_1 + 1 #Hold the channel of other BS for 3 sec
                                                HO_attempt_BS21 = HO_attempt_BS21 + 1 #Update HO Attempt
                                            User_Data[i][5] = User_Data[i][5] + 1 #Counter of 3 sec for that user as HO takes time
                                            i = i + 1
                                            raise StopLookingForThings()
                                        
                                        #Update the paramters for successful HO
                                        User_Data[i][5] = 0
                                        Active_Call_BS_2 = Active_Call_BS_2 - 1
                                        User_Data[i][4] = 'HO_to_BS_1'
                                        User_Data[i][3] = 'Serving_BS_1'
                                        User_Data[i][8] = 'Handover_Completed'
                                        HO_Succ_BS21 = HO_Succ_BS21 + 1
                                    else:
                                        #Update the paramters for Failed HO
                                        HO_attempt_BS21 = HO_attempt_BS21 + 1
                                        HO_Fail_BS21 = HO_Fail_BS21 + 1
                                        Call_Block_Cap1 = Call_Block_Cap1 + 1
                    else: #If user's call timer has ended
                        #Complete the call as succeful connection and free the channel of whichever BS is was connected
                        User_Data[i][0] = 'False'
                        Succ_complete_call = Succ_complete_call + 1
                        if(User_Data[i][3] == 'Serving_BS_1'):
                            Active_Call_BS_1 = Active_Call_BS_1 - 1
                        elif(User_Data[i][3] == 'Serving_BS_2'):
                            Active_Call_BS_2 = Active_Call_BS_2 - 1
                        User_Data[i][8] = 'Call_Completed'

                        #NOTE: introduce the counter for number of succesfful call  
        except StopLookingForThings:
            pass
    Step_Size = Step_Size + 1

#Exporting the data to an excel file
df = pd.DataFrame(User_Data)
df_trans = df.T
df_trans['bs_1'] = pd.Series(RSL_BS_1)
df_trans['bs_2'] = pd.Series(RSL_BS_2)
df_trans['initial_loc'] = init_loc_arr
df_trans['initial_call_dur'] = newarr
df_trans['updated_call_dur'] = User_Call_Duration
writer = pd.ExcelWriter('Test_A.xlsx', engine='xlsxwriter')
df_trans.to_excel(writer, sheet_name='Sheet1')
writer.save()

#Collect the counters at the end of simulation
print("Active Call BS 1 = ",Active_Call_BS_1)
print("Active Call BS2 = ",Active_Call_BS_2)
print("Call attempt counter = ",Call_attempt_counter) 
print("Succ call connection = ",Succ_call_conn) 
print("Succ call complete = ",Succ_complete_call)
print("HO attempt by BS1 = ",HO_attempt_BS12)
print("HO attempt by BS2 = ",HO_attempt_BS21)
print("HO Succ by BS1 = ",HO_Succ_BS12)
print("HO Succ by BS2 = ",HO_Succ_BS21)
print("HO fail by BS1 = ",HO_Fail_BS12)
print("HO fail by BS2 = ",HO_Fail_BS21)
print("Call block of due to capacity BS 1 = ",Call_Block_Cap1)
print("Call block of due to capacity BS 2 =",Call_Block_Cap2)
print("Drop Call BS1 = ",Drop_Call_BS1)
print("Drop Call BS2 = ",Drop_Call_BS2)
print("Call block due to strength BS 1 = ",Call_Block_Strength1)
print("Call block due to strength BS 2 = ",Call_Block_Strength2)

