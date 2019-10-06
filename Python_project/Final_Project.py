import numpy as np
import Utils as utils
import random as random
import pandas as pd
class StopLookingForThings(Exception): pass



#Paramters for Base Stations
Dist_of_BS = 12 #in kms
N_Channel_BS = 30 #Each sector
#NOTE: sim_hour to be entered by user
sim_hour = 1
index_1 = 0
index_2 = 0
#Paramteres for Mobile Station
RSL_Thresh = -102 #dBm
N_of_Users = 1000 # (to be requested by user)
Call_rate = 1 #1 call per hour
Av_Call_Duration = 15 # 3 minutes per call
Mob_Speed = 15 #m/s (to be requeseted by user)
HO_Timer = 3
SHAD_RES = 10 #in mtrs
Step_Size = 1
simulation_time = sim_hour * 3600
#prob of call (units in secs)
prob_of_call = (Call_rate * (Step_Size/60))
prob = 0.5
#print(prob_of_call)

dist_by_user = Mob_Speed * Step_Size

dist_cov_by_user_in_step = Mob_Speed * Step_Size
#initiate dictionary
User_Data = {}

#NOTE: TBD - Check this
#init_call_dur = [0]*N_of_Users
User_Call_Duration = np.random.exponential(180,N_of_Users)
init_call_dur = User_Call_Duration
print(init_call_dur)

print("\n",User_Call_Duration)

Location_arr = np.random.uniform(0,12000,N_of_Users) #NOTE TBD
init_loc_arr = Location_arr
for i in range(0,N_of_Users):#NOTE TBD
    #0th - is call set up or not
    #1st - location of the user
    #2nd - direction in which the user is moving
    #3rd - Serving Base station
    #4th - Block call counter
    #5th - Call Drop Counter
    #6th - User Archived or not
    User_Data[i] = ['False',Location_arr[i],'Stationary','Null','Null',0,0,'Null']

#print("Initial dict = ",User_Data)
Call_attempt_counter = 0
Succ_call_conn = 0
Succ_complete_call = 0
HO_attempt = 0
HO_Succ = 0
HO_Fail_1 = 0
HO_Fail_2 = 0
Cap_Block_1 = 0
Cap_Block_2 = 0

Active_Call_BS_1 = 0
Active_Call_BS_2 = 0
User_Archive_list = []

Step_Size = 1 
RSL_BS_1 = [0]*N_of_Users
RSL_BS_2 = [0]*N_of_Users
#simulation_time = 3

# NOTE: Known issue- larger distance but still RSL is really good. (+ve)
while(Step_Size <= simulation_time):
    for i in range(0,N_of_Users):#NOTE TBD
        try:
            #print("i = ", i)
            print("Step = ",Step_Size)
            if(User_Data[i][7] == 'User_Archived'):
                i = i + 1
                raise StopLookingForThings()
            else:

                if(User_Data[i][0] == 'False'):
                    gen = np.arange(0.0,1.0,0.01)
                    user_prob = random.choice(gen)
                    if(user_prob <= prob):
                        i = i + 1
                        raise StopLookingForThings()
                    else:
                        Call_attempt_counter = Call_attempt_counter + 1
                        if(User_Data[i][1] >12000):
                            User_Archive_list.append(User_Data[i])
                            User_Data[i][7] = 'User_Archived'
                            User_Data[i][0] = 'False'
                            User_Call_Duration[i] = 0
                            Succ_complete_call = Succ_complete_call + 1
                            i = i + 1
                            raise StopLookingForThings()

                        elif(User_Data[i][1] < 0):
                            User_Archive_list.append(User_Data[i])
                            User_Data[i][7] = 'User_Archived'
                            User_Data[i][0] = 'False'
                            User_Call_Duration[i] = 0
                            Succ_complete_call = Succ_complete_call + 1
                            i = i + 1
                            raise StopLookingForThings()  
                        else:
                            RSL_BS_1[i] = utils.calc_RSL(User_Data[i][1])
                            RSL_BS_2[i] = utils.calc_RSL(12000 - User_Data[i][1])
                        if(RSL_BS_1[i] > RSL_BS_2[i]):
                            if(RSL_BS_1[i] >= RSL_Thresh):
                                if(Active_Call_BS_1 < N_Channel_BS and Active_Call_BS_1 > 0 ):
                                     #Call setup marked as 1
                                    if(User_Call_Duration[i] != 0 and User_Data[i][1] > 0 and User_Data[i][1] <=11999 ):
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
                                if(Active_Call_BS_2 < N_Channel_BS and Active_Call_BS_2 >0):
                                    if(User_Call_Duration[i] != 0 and User_Data[i][1] > 0 and User_Data[i][1] <=11999 ):
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
                            
                    if(User_Data[i][1] >12000  and User_Call_Duration[i] != 0 ):
                        Active_Call_BS_2 = Active_Call_BS_2 - 1
                        User_Data[i][0] = 'False'
                        User_Call_Duration[i] = 0
                        #User_Data[i][1] = 11999
                        User_Archive_list.append(User_Data[i])
                        User_Data[i][7] = 'User_Archived'
                        Succ_complete_call = Succ_complete_call + 1
                        i = i + 1
                        raise StopLookingForThings()
                        
                    elif(User_Data[i][1] < 0 and User_Call_Duration[i] != 0 ):
                        Active_Call_BS_1 = Active_Call_BS_1 - 1
                        User_Data[i][0] = 'False'
                        User_Call_Duration[i] = 0
                        #User_Data[i][1] = 1
                        User_Archive_list.append(User_Data[i])
                        User_Data[i][7] = 'User_Archived'
                        Succ_complete_call = Succ_complete_call + 1
                        #break
                        i = i + 1
                        raise StopLookingForThings()                
                    else:
                        RSL_BS_1[i] = utils.calc_RSL(User_Data[i][1])
                        RSL_BS_2[i] = utils.calc_RSL(12000 - User_Data[i][1])
                    if(User_Call_Duration[i] != 0 ):
                        User_Call_Duration[i] = User_Call_Duration[i] - 1
                        if (User_Data[i][3] == 'Serving_BS_1'):
                            if(RSL_BS_1[i] < RSL_Thresh):
                                User_Data[i][5] = User_Data[i][5] + 1
                                Active_Call_BS_1 = Active_Call_BS_1 - 1
                            elif(RSL_BS_1[i] >= RSL_Thresh):
                                if(RSL_BS_2[i] > RSL_BS_1[i]):
                                    #increase counter for HO
                                    if(Active_Call_BS_2 < N_Channel_BS and Active_Call_BS_2 >0 ):
                                        #Active_Call_BS_2 = Active_Call_BS_2 + 1
                                        HO_attempt = HO_attempt + 1
                                        #NOTE: Doubtful 
                                        while(index_1 < HO_Timer):
                                            index_1 = index_1 + 1
                                            i = i + 1
                                            raise StopLookingForThings()
                                        
                                        index_1 = 0
                                        Active_Call_BS_1 = Active_Call_BS_1 - 1
                                        User_Data[i][4] = 'HO_to_BS_2'
                                        User_Data[i][3] = 'Serving_BS_2'
                                        Active_Call_BS_2 = Active_Call_BS_2 + 1
                                        HO_Succ = HO_Succ + 1
                                        #NOTE: counter for succesful HO
                                    else:
                                        #NOTE counter for HO failure
                                        HO_Fail_1 = HO_Fail_1 + 1
                                        Cap_Block_2 = Cap_Block_2 + 1

                        elif(User_Data[i][3] == 'Serving_BS_2'):
                            if(RSL_BS_2[i] < RSL_Thresh):
                                User_Data[i][5] = User_Data[i][5] + 1
                                Active_Call_BS_2 = Active_Call_BS_2 - 1
                            elif(RSL_BS_2[i] >= RSL_Thresh):
                                if(RSL_BS_1[i] > RSL_BS_2[i]):
                                    #increase counter for HO
                                    if(Active_Call_BS_1 < N_Channel_BS):
                                        #Active_Call_BS_1 = Active_Call_BS_1 + 1
                                        while(index_2 < HO_Timer):
                                            index_2 = index_2 + 1
                                            i = i + 1
                                            raise StopLookingForThings()
                                        
                                        index_2 = 0
                                        Active_Call_BS_2 = Active_Call_BS_2 - 1
                                        User_Data[i][4] = 'HO_to_BS_1'
                                        User_Data[i][3] = 'Serving_BS_1'
                                        Active_Call_BS_1 = Active_Call_BS_1 + 1
                                        #NOTE: counter for succesful HO
                                        HO_Succ = HO_Succ + 1
                                    else:
                                        #NOTE counter for HO failure
                                        HO_Fail_2 = HO_Fail_2 + 1
                                        Cap_Block_1 = Cap_Block_1 + 1

                        elif(User_Data[i][1] > 11999 or User_Data[i][1] <= 1 ):
                            User_Data[i][0] = 'False'
                            if(User_Data[i][3] == 'Serving_BS_1'):
                                Active_Call_BS_1 = Active_Call_BS_1 - 1
                            elif(User_Data[i][3] == 'Serving_BS_2'):
                                Active_Call_BS_2 = Active_Call_BS_2 - 1
                    else:
                        User_Data[i][0] = 'False'
                        Succ_complete_call = Succ_complete_call + 1
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
df_trans['initial_call_dur'] = init_call_dur
writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
df_trans.to_excel(writer, sheet_name='Sheet1')
writer.save()
'''
print(Active_Call_BS_1)
print(Active_Call_BS_2)
print(HO_Fail_1 + HO_Fail_2)
'''