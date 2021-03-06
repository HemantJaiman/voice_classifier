import csv
import math
import scipy
#from numpy import random as r
#r.normal()
c=0
mc=0
fc=0
sum_male_mf=0
sum_female_mf=0
mean_freq_male_mvu=0
mean_freq_female_mvu=0
with open('voice.csv' , 'r') as people_file:
    final_data=list(csv.DictReader(people_file))
for one_person in final_data[0:2999]:
    one_person=dict(one_person)
    if one_person['label'] == 'male':
       mc=mc+1
       sum_male_mf=sum_male_mf+float(one_person['meanfreq'])
    else:
       fc=fc+1
       sum_female_mf=sum_female_mf+float(one_person['meanfreq'])
mean_freq_male_mvu=sum_male_mf/mc
mean_freq_male_mvu=sum_female_mf/fc

sum_male_mf=0
sum_female_mf=0

var_mvu_male=0
var_mvu_female=0

for one_person in final_data[0:2999]:
    one_person = dict(one_person)
    if one_person['label']=='male':
        sum_male_mf=sum_male_mf+math.pow((float(one_person['meanfreq'])-mean_freq_male_mvu),2)
    else:
        sum_female_mf=sum_female_mf+math.pow((float(one_person['meanfreq'])-mean_freq_female_mvu),2)

var_mvu_male=sum_male_mf/mc
var_mvu_female=sum_female_mf/fc

#going to compute hte prior probability : p(voice is male/mean freq)
#going to compute hte prior probability : p(voice is female/mean freq)
#posterior_male is actually p(mean freq| voice is male)
#posterior_female is actually p(mean freq| voice is female)

#posterior_male = scipy.stats.norm(mean_freq_male_mvu, var_mvu_male).pdf(float(one_person['meanfreq']))

correct_class=0
for one_person in final_data[3000:3167]:
    one_person = dict(one_person)

    posterior_male=(1/(math.sqrt(2*3.14)*math.sqrt(var_mvu_male)))*math.exp(-(math.pow((float(one_person['meanfreq'])-mean_freq_male_mvu),2)/(2*var_mvu_male)))

    posterior_female =(1/(math.sqrt(2*3.14) * math.sqrt(var_mvu_female)))*math.exp(-(math.pow((float(one_person['meanfreq'])-mean_freq_female_mvu),2)/(2*var_mvu_female)))


    prior_male=(posterior_male*(mc/len(final_data)))/(posterior_male*(mc/len(final_data)))+(posterior_female*(fc/len(final_data)))

    prior_female = (posterior_female * (fc / len(final_data))) / (posterior_male * (mc / len(final_data))) + (posterior_female * (fc / len(final_data)))


    if prior_male > prior_female and one_person['label'] == 'male':
        correct_class=correct_class+1
    elif  prior_male < prior_female and one_person['label'] == 'female':
        correct_class=correct_class+1


print("accuracy of our bayes classifier is :"+str((correct_class/168)*100))
