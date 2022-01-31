#amazon_reviews_us_Digital_Music_Purchase_v1_00
from audioop import avg
import datetime


total_indexed_docs = 798864
indexMergeTime = "0:49:04.877800"

res = [{"n_results": 6874,
"n_relevant": 59,
"n_relevant_retrieved": 59,
"SearchTime": "0:01:12.591025"
},{"n_results": 2139,
"n_relevant": 79,
"n_relevant_retrieved": 79,
"SearchTime": "0:02:39.371756"
},{"n_results": 901,
"n_relevant": 87,
"n_relevant_retrieved": 87,
"SearchTime": "0:04:12.309938"
},{"n_results": 3717,
"n_relevant": 60,
"n_relevant_retrieved": 61,
"SearchTime": "0:05:23.969928"
},{"n_results": 5907,
"n_relevant": 70,
"n_relevant_retrieved": 70,
"SearchTime": "0:06:53.158113"
},{"n_results": 5908,
"n_relevant": 75,
"n_relevant_retrieved": 75,
"SearchTime": "0:08:16.718429"
},{"n_results": 283,
"n_relevant": 68,
"n_relevant_retrieved": 68,
"SearchTime": "0:09:33.819806"
},{"n_results": 5908,
"n_relevant": 73,
"n_relevant_retrieved": 73,
"SearchTime": "0:10:55.155038"
},{"n_results": 3053,
"n_relevant": 79,
"n_relevant_retrieved": 79,
"SearchTime": "0:12:21.923505"
},{"n_results": 963,
"n_relevant": 86,
"n_relevant_retrieved": 86,
"SearchTime": "0:13:58.384297"
},{"n_results": 63,
"n_relevant": 54,
"n_relevant_retrieved": 54,
"SearchTime": "0:15:04.700898"
},{"n_results": 229,
"n_relevant": 66,
"n_relevant_retrieved": 66,
"SearchTime": "0:16:23.876071"
},{"n_results": 3423,
"n_relevant": 89,
"n_relevant_retrieved": 89,
"SearchTime": "0:18:09.456466"
},{"n_results": 8240,
"n_relevant": 75,
"n_relevant_retrieved": 75,
"SearchTime": "0:19:34.100277"
},{"n_results": 3718,
"n_relevant": 82,
"n_relevant_retrieved": 82,
"SearchTime": "0:21:05.956604"
}]
search_times = []
for result in res:
    precision = result["n_relevant"] / result["n_results"]
    recall =  result["n_relevant_retrieved"] / result["n_relevant"] 
    f_measure = 2*precision*recall/(precision + recall)
    times = result["SearchTime"].split(":")
    search_times.append(datetime.timedelta(hours=int(times[0]), minutes=int(times[1]), seconds=int(times[2].split(".")[0]), milliseconds=int(times[2].split(".")[1])))
    print("Precision: " + str(precision))
    print("recall: "+str(recall))
    print("f_measure: "+str(f_measure))
avg_q_throughput = datetime.timedelta(0)
for time in search_times:
    avg_q_throughput += time
avg_q_throughput /= len(search_times)
median_q_latency = None
if len(search_times) % 2 == 0:
    median_q_latency =  (search_times[int(len(search_times)/2)] + times[int(len(search_times)/2)-1]) / 2
else:
    median_q_latency =  search_times[int(len(search_times)/2)]
print("avg_q_throughput: "+str(avg_q_throughput))
print("median_q_latency: "+str(median_q_latency))