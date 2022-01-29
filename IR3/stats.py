#amazon_reviews_us_Digital_Music_Purchase_v1_00

total_indexed_docs = 798864
indexMergeTime = "0:49:04.877800"
#Total indexed docs: 798864
#IndexMergeTime: 0:49:08.311165
#n_results: 6874
#n_relevant: 59
#n_relevant_retrieved: 59
#SearchTime: 0:01:12.591025
#n_results: 2139
#n_relevant: 79
#n_relevant_retrieved: 79
#SearchTime: 0:02:39.371756
#n_results: 901
#n_relevant: 87
#n_relevant_retrieved: 87
#SearchTime: 0:04:12.309938
#n_results: 3717
#n_relevant: 60
#n_relevant_retrieved: 61
#SearchTime: 0:05:23.969928
#n_results: 5907
#n_relevant: 70
#n_relevant_retrieved: 70
#SearchTime: 0:06:53.158113
#n_results: 5908
#n_relevant: 75
#n_relevant_retrieved: 75
#SearchTime: 0:08:16.718429
#n_results: 283
#n_relevant: 68
#n_relevant_retrieved: 68
#SearchTime: 0:09:33.819806
#n_results: 5908
#n_relevant: 73
#n_relevant_retrieved: 73
#SearchTime: 0:10:55.155038
#n_results: 3053
#n_relevant: 79
#n_relevant_retrieved: 79
#SearchTime: 0:12:21.923505
#n_results: 963
#n_relevant: 86
#n_relevant_retrieved: 86
#SearchTime: 0:13:58.384297
#n_results: 63
#n_relevant: 54
#n_relevant_retrieved: 54
#SearchTime: 0:15:04.700898
#n_results: 229
#n_relevant: 66
#n_relevant_retrieved: 66
#SearchTime: 0:16:23.876071
#n_results: 3423
#n_relevant: 89
#n_relevant_retrieved: 89
#SearchTime: 0:18:09.456466
#n_results: 8240
#n_relevant: 75
#n_relevant_retrieved: 75
#SearchTime: 0:19:34.100277
#n_results: 3718
#n_relevant: 82
#n_relevant_retrieved: 82
#SearchTime: 0:21:05.956604

res = [{
"n_results": 6874,
"n_relevant": 59,
"SearchTime": "0:00:59.369260"
},
{
"n_results": 2139,
"n_relevant": 79,
"SearchTime": "0:02:09.172854"
},
{
"n_results": 901,
"n_relevant": 87,
"SearchTime": "0:03:24.266624"
},
{
"n_results": 3717,
"n_relevant": 60,
"SearchTime": "0:04:22.542640"
},
{
"n_results": 5907,
"n_relevant": 70,
"SearchTime": "0:05:33.282440"
},
{
"n_results": 5908,
"n_relevant": 75,
"SearchTime": "0:06:41.901766"
},
{
"n_results": 283,
"n_relevant": 68,
"SearchTime": "0:07:42.609328"
},
{
"n_results": 5908,
"n_relevant": 73,
"SearchTime": "0:08:48.056957"
},
{
"n_results": 3053,
"n_relevant": 79,
"SearchTime": "0:09:58.198623"
},
{
"n_results": 963,
"n_relevant": 86,
"SearchTime": "0:11:13.339406"
},
{
"n_results": 63,
"n_relevant": 54,
"SearchTime": "0:12:06.576296"
},
{
"n_results": 229,
"n_relevant": 66,
"SearchTime": "0:13:12.035917"
},
{
"n_results": 3423,
"n_relevant": 89,
"SearchTime": "0:14:35.405538"
},
{
"n_results": 8240,
"n_relevant": 75,
"SearchTime": "0:15:45.936291"
},
{
"n_results": 3718,
"n_relevant": 82,
"SearchTime": "0:16:59.977828"
}]
for result in res:
    precision = result["n_relevant"] / (result["n_relevant"] + result["n_results"])
    recall =  result["n_relevant"] / (result["n_relevant"] + result["n_results"])
    