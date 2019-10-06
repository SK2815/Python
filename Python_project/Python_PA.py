
import numpy as np
import Utils_A as utils
import random as random
import pandas as pd
class StopLookingForThings(Exception): pass

#Paramters for Base Stations
Dist_of_BS = int(input("Enter the distance: ")) #in kms
BS_dist = Dist_of_BS * 1000
N_Channel_BS = 30 #Each sector
#NOTE: sim_hour to be entered by user
sim_hour = int(input("Enter the simulation hour: "))
index_1 = 0
index_2 = 0
#Paramteres for Mobile Station
RSL_Thresh = -102 #dBm
N_of_Users = int(input("Enter the number of Users: ")) # (to be requested by user)
Call_rate = 1 #1 call per hour
Av_Call_Duration = 15 # 3 minutes per call
Mob_Speed = int(input("Enter the speed of the mobile: ")) #m/s (to be requeseted by user)
HO_Timer = 3
SHAD_RES = 10 #in mtrs
Step_Size = 1
simulation_time = sim_hour * 100
#prob of call (units in secs)
prob_of_call = (Call_rate * (Step_Size/3600))

dist_by_user = Mob_Speed * Step_Size

#initiate dictionary
User_Data = {}

#NOTE: TBD - Check this
#init_call_dur = [0]*N_of_Users
init_call_dur = np.random.exponential(180,N_of_Users)
newarr = init_call_dur.round()
#print(newarr)
User_Call_Duration = list(newarr)
#print(init_call_dur)

#print("\n",User_Call_Duration)

Location_arr = np.random.uniform(0,BS_dist,N_of_Users) #NOTE TBD
#Location_arr = [0]*N_of_Users
init_loc_arr = Location_arr
for i in range(0,N_of_Users):#NOTE TBD
    #0th - is call set up or not
    #1st - location of the user
    #2nd - direction in which the user is moving
    #3rd - Serving Base station
    #4th - HO status to BS
    #5th - Call Block counter
    #6th - Call Drop Counter
    #7th - User Archived or not
    #8th - Handover ongoing or completed status
    User_Data[i] = ['False',Location_arr[i],'Stationary','Null','Null',0,0,'Null','Null']



#print("Initial dict = ",User_Data)
Call_attempt_counter = 0
Succ_call_conn = 0
Succ_complete_call = 0
HO_attempt_BS12 = 0
HO_attempt_BS21  = 0
HO_Succ_BS12 = 0
HO_Succ_BS21 = 0
HO_Fail_BS12 = 0
HO_Fail_BS21 = 0
Cap_Block_BS1 = 0
Cap_Block_BS2 = 0

Active_Call_BS_1 = 0
Active_Call_BS_2 = 0
User_Archive_list = []

Step_Size = 1 
#NOTE: Change it to dictionary or other data structure which is faster than list 
RSL_BS_1 = [0]*N_of_Users
RSL_BS_2 = [0]*N_of_Users
#simulation_time = 3


def calc_Shadowing(BS_dist):
    random_val = np.random.normal(0, 2, BS_dist)
    return random_val


#NOTE: Convert ndarrays to faster data structure
Shadowing_BS_1 = calc_Shadowing(BS_dist)
Shadowing_BS_2 = calc_Shadowing(BS_dist)


# NOTE: Known issue- larger distance but still RSL is really good. (+ve)
while(Step_Size <= simulation_time):
    print("Step = ",Step_Size)
    for i in range(0,N_of_Users):#NOTE TBD
        try:
            #print("i = ", i)
            
            if(User_Data[i][7] == 'User_Archived'):
                i = i + 1
                raise StopLookingForThings()
            else:
                
                if(User_Data[i][0] == 'False'):
                    gen = np.arange(0.0,3600,0.00001)
                    user_prob = random.choice(gen)
                    if(user_prob <= prob_of_call):
                        i = i + 1
                        raise StopLookingForThings()
                    else:
                        print(user_prob)
                        Call_attempt_counter = Call_attempt_counter + 1
                        if(User_Data[i][1] >BS_dist):
                            User_Archive_list.append(User_Data[i])
                            User_Data[i][7] = 'User_Archived'
                            User_Data[i][0] = 'False'
                            User_Call_Duration[i] = 0
                            #Succ_complete_call = Succ_complete_call + 1
                            i = i + 1
                            raise StopLookingForThings()

                        elif(User_Data[i][1] < 0):
                            User_Archive_list.append(User_Data[i])
                            User_Data[i][7] = 'User_Archived'
                            User_Data[i][0] = 'False'
                            User_Call_Duration[i] = 0
                            #Succ_complete_call = Succ_complete_call + 1
                            i = i + 1
                            raise StopLookingForThings()  
                        else:
                            #print("In else")
                            RSL_BS_1[i] = utils.calc_RSL(User_Data[i][1],Shadowing_BS_1)
                            RSL_BS_2[i] = utils.calc_RSL(BS_dist - User_Data[i][1],Shadowing_BS_2)
                        if(RSL_BS_1[i] > RSL_BS_2[i]):
                            if(RSL_BS_1[i] >= RSL_Thresh):
                                #print(Active_Call_BS_1)
                                if(Active_Call_BS_1 < N_Channel_BS and Active_Call_BS_1 >= 0 ):
                                     #Call setup marked as 1
                                    if(User_Call_Duration[i] > 0 and User_Data[i][1] > 0 and User_Data[i][1] <=(BS_dist-1) ):
                                        User_Call_Duration[i] = User_Call_Duration[i] - 1
                                        User_Data[i][1] = User_Data[i][1] + dist_by_user
                                        User_Data[i][2] = 'East'
                                        User_Data[i][3] = 'Serving_BS_1'
                                        Active_Call_BS_1 = Active_Call_BS_1 + 1
                                        Succ_call_conn = Succ_call_conn + 1
                                        User_Data[i][0] = 'True'
                                    else:
                                        User_Data[i][0] = 'False'
                                elif(Active_Call_BS_1 >= N_Channel_BS):
                                    User_Data[i][5] = User_Data[i][5] + 1
                        elif(RSL_BS_2[i] > RSL_BS_1[i]): 
                            if(RSL_BS_2[i] >= RSL_Thresh):#NOTE: complete
                                #print(Active_Call_BS_2)
                                if(Active_Call_BS_2 < N_Channel_BS and Active_Call_BS_2 >= 0):
                                    if(User_Call_Duration[i] > 0 and User_Data[i][1] > 0 and User_Data[i][1] <=(BS_dist-1) ):
                                        User_Call_Duration[i] = User_Call_Duration[i] - 1
                                        User_Data[i][0] = 'True' #Call setup marked as 1
                                        User_Data[i][1] = User_Data[i][1] - dist_by_user
                                        User_Data[i][2] = 'West'
                                        User_Data[i][3] = 'Serving_BS_2'
                                        Active_Call_BS_2 = Active_Call_BS_2 + 1
                                        Succ_call_conn = Succ_call_conn + 1
                                    else:
                                        #terminate the call here.
                                        User_Data[i][0] = 'False'
                                        #Active_Call_BS_2 = Active_Call_BS_2 - 1
                                elif(Active_Call_BS_2 >= N_Channel_BS):
                                    User_Data[i][5] = User_Data[i][5] + 1
                elif(User_Data[i][0] == 'True'):
                    #NOTE: Write code here when the call is ongoing
                    if(User_Data[i][2] == 'West'):
                        User_Data[i][1] = User_Data[i][1] - dist_by_user
                    elif(User_Data[i][2] == 'East'):
                        User_Data[i][1] = User_Data[i][1] + dist_by_user   
                            
                    if(User_Data[i][1] >BS_dist  and User_Call_Duration[i] > 0 and User_Data[i][3] == 'Serving_BS_2' ):
                        Active_Call_BS_2 = Active_Call_BS_2 - 1
                        User_Data[i][0] = 'False'
                        User_Call_Duration[i] = 0
                        #User_Data[i][1] = 11999
                        User_Archive_list.append(User_Data[i])
                        User_Data[i][7] = 'User_Archived'
                        User_Data[i][8] = 'Call_Completed as user moved past the BS_2'
                        Succ_complete_call = Succ_complete_call + 1
                        i = i + 1
                        raise StopLookingForThings()
                        
                    elif(User_Data[i][1] < 0 and User_Call_Duration[i] > 0 and User_Data[i][3] == 'Serving_BS_1'):
                        Active_Call_BS_1 = Active_Call_BS_1 - 1
                        User_Data[i][0] = 'False'
                        User_Call_Duration[i] = 0
                        #User_Data[i][1] = 1
                        User_Archive_list.append(User_Data[i])
                        User_Data[i][7] = 'User_Archived'
                        User_Data[i][8] = 'Call_Completed as user moved past the BS_1'
                        Succ_complete_call = Succ_complete_call + 1
                        #break
                        i = i + 1
                        raise StopLookingForThings()                
                    else:
                        RSL_BS_1[i] = utils.calc_RSL(User_Data[i][1],Shadowing_BS_1)
                        RSL_BS_2[i] = utils.calc_RSL(BS_dist - User_Data[i][1],Shadowing_BS_2)
                    if(User_Call_Duration[i] > 0 ):
                        User_Call_Duration[i] = User_Call_Duration[i] - 1
                        if (User_Data[i][3] == 'Serving_BS_1'):
                            if(RSL_BS_1[i] < RSL_Thresh):
                                User_Data[i][5] = User_Data[i][5] + 1
                                Active_Call_BS_1 = Active_Call_BS_1 - 1
                            elif(RSL_BS_1[i] >= RSL_Thresh):
                                if(RSL_BS_2[i] > RSL_BS_1[i]):
                                    #increase counter for HO
                                    if(Active_Call_BS_2 < N_Channel_BS and Active_Call_BS_2 >=0 ):
                                        #Active_Call_BS_2 = Active_Call_BS_2 + 1
                                        HO_attempt_BS12 = HO_attempt_BS12 + 1
                                        #NOTE: Doubtful 
                                        while(index_1 < HO_Timer):
                                            index_1 = index_1 + 1
                                            User_Data[i][8] = 'Handover_Ongoing'
                                            i = i + 1
                                            raise StopLookingForThings()
                                        
                                        index_1 = 0
                                        Active_Call_BS_1 = Active_Call_BS_1 - 1
                                        User_Data[i][4] = 'HO_to_BS_2'
                                        User_Data[i][3] = 'Serving_BS_2'
                                        User_Data[i][8] = 'Handover_Completed'
                                        Active_Call_BS_2 = Active_Call_BS_2 + 1
                                        HO_Succ_BS12 = HO_Succ_BS12 + 1
                                        #NOTE: counter for succesful HO
                                    else:
                                        #NOTE counter for HO failure
                                        HO_Fail_BS12 = HO_Fail_BS12 + 1
                                        Cap_Block_BS2 = Cap_Block_BS2 + 1

                        elif(User_Data[i][3] == 'Serving_BS_2'):
                            if(RSL_BS_2[i] < RSL_Thresh):
                                User_Data[i][5] = User_Data[i][5] + 1
                                Active_Call_BS_2 = Active_Call_BS_2 - 1
                            elif(RSL_BS_2[i] >= RSL_Thresh):
                                if(RSL_BS_1[i] > RSL_BS_2[i]):
                                    #increase counter for HO
                                    if(Active_Call_BS_1 < N_Channel_BS and Active_Call_BS_1 >=0):
                                        #Active_Call_BS_1 = Active_Call_BS_1 + 1
                                        HO_attempt_BS21 = HO_attempt_BS21 + 1
                                        while(index_2 < HO_Timer):
                                            index_2 = index_2 + 1
                                            User_Data[i][8] = 'Handover_Ongoing'
                                            i = i + 1
                                            raise StopLookingForThings()
                                        
                                        index_2 = 0
                                        Active_Call_BS_2 = Active_Call_BS_2 - 1
                                        User_Data[i][4] = 'HO_to_BS_1'
                                        User_Data[i][3] = 'Serving_BS_1'
                                        User_Data[i][8] = 'Handover_Completed'
                                        Active_Call_BS_1 = Active_Call_BS_1 + 1
                                        #NOTE: counter for succesful HO
                                        HO_Succ_BS21 = HO_Succ_BS21 + 1
                                    else:
                                        #NOTE counter for HO failure
                                        HO_Fail_BS21 = HO_Fail_BS21 + 1
                                        Cap_Block_BS1 = Cap_Block_BS1 + 1
                        #NOTE: KNOWN BIG ISSUE FOR ACTIVE CALL COUNTERS...
                        elif(User_Data[i][1] > (BS_dist-1) or User_Data[i][1] <= 1 ):
                            User_Data[i][0] = 'False'
                            if(User_Data[i][3] == 'Serving_BS_1'):
                                Active_Call_BS_1 = Active_Call_BS_1 - 1
                            elif(User_Data[i][3] == 'Serving_BS_2'):
                                Active_Call_BS_2 = Active_Call_BS_2 - 1
                    else:
                        User_Data[i][0] = 'False'
                        Succ_complete_call = Succ_complete_call + 1
                        if(User_Data[i][3] == 'Serving_BS_1'):
                            Active_Call_BS_1 = Active_Call_BS_1 - 1
                        elif(User_Data[i][3] == 'Serving_BS_2'):
                            Active_Call_BS_2 = Active_Call_BS_2 - 1

                        if(User_Data[i][8] == 'Handover_Ongoing' or User_Data[i][8] == 'Handover_Completed'):
                            User_Data[i][8] = 'Call_Completed'

                        #NOTE: introduce the counter for number of succesfful call  
        except StopLookingForThings:
            pass
    Step_Size = Step_Size + 1

serv_list = []
for i in range(N_of_Users):
    serv_list.append(User_Data[i][3])



df = pd.DataFrame(User_Data)


#df.append(df_1,ignore_index=True)
#df.append(df_2,ignore_index= True)
#pd.DataFrame(Location_arr).to_excel('loc.xlsx', header=False, index=False)
#pd.DataFrame(RSL_BS_1).to_excel('bs_1.xlsx', header=False, index=False)
#pd.DataFrame(RSL_BS_2).to_excel('bs_2.xlsx', header=False, index=False)
#pd.DataFrame(serv_list).to_excel('serv_list.xlsx', header=False, index=False)
df_trans = df.T
df_trans['bs_1'] = RSL_BS_1
df_trans['bs_2'] = RSL_BS_2
df_trans['initial_loc'] = init_loc_arr
df_trans['initial_call_dur'] = newarr
df_trans['updated_call_dur'] = User_Call_Duration
writer = pd.ExcelWriter('Test_A.xlsx', engine='xlsxwriter')
df_trans.to_excel(writer, sheet_name='Sheet1')
writer.save()

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
print("Cap block of BS1 = ",Cap_Block_BS1)
print("Cap block of BS2 = ",Cap_Block_BS2)




