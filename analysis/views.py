import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from analysis import models
from analysis.tool.splicing import Splicing


class AssemblyView(View):
    def get_tableData(self, data_list):
        tableData = {}
        for data in data_list:
            tableData[data['name']] = data['data']

        tableData['Na'] = 1.2
        return tableData

    def get(self, request):
        return render(request, 'assembly.html')

    def get_res_info(self, info):
        res_info = {
            'min': info.get('min'),
            'max': info.get('max'),
            'range': info.get('range'),
            'mean': info.get('mean'),
            'std': info.get('std')
        }

        if info.get('tail'):
            res_info['tail'] = info.get('tail')

        tem_res = []
        for key, value in res_info.items():
            tem = {
                'key': key,
                'value': value,
            }
            tem_res.append(tem)
        return tem_res

    def post(self, request):
        data = json.loads(request.body)

        ion = data.pop('tableData')
        ion = self.get_tableData(ion)
        # add ion to data (dits)
        data.update(ion)
        data['gene'] = data['gene'].replace('\n', '').replace(' ', '').replace('\r', '')
        # print(data)

        # add to db
        # models.GeneInfo.objects.create(email=data['email'], gene_len=data['geneLen'],
        #                                pools=data['pools'], min_len=data['minLen'], max_len=data['maxLen'])
        print(data)
        splic = Splicing(data)
        next_cal, info = splic.cal()

        # add cal info to context
        tem_res = self.get_res_info(info)

        context = {
            'info': info.get('result'),
            'resInfo': tem_res,
            'nextCal': next_cal
        }
        # print(context)
        # if data.get('verification') == 'Yes':
        #
        #     conc = data['concentrations'] * 1e-8
        #     # 分析过程
        #     analy = Analysis(next_cal[0], next_cal[1][1:], next_cal[2], data['temperature'], conc)
        #     analy_info = analy.analysis_two()
        #     analy_info.update(analy.analysis_three())
        #
        #     analy_info_list = []
        #     for key, value in analy_info.items():
        #         analy_info_list.append({
        #             'key': key,
        #             'value': value,
        #         })
        #     context['analyInfo'] = analy_info_list

        arr = [context]
        # print(arr)
        context = {'arr': arr}
        return JsonResponse(context)