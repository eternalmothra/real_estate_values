from lxml import html
import requests
import csv as csv

def main():
    zwsid = #put your zillow key here
    csv_file_input =csv.reader(open('elf_addresses.csv', 'rb'))
    answer_file = open ('property_values.csv', 'wb')
    answer_file_object = csv.writer(answer_file)
    header = csv_file_input.next()
    
    answer_file_object.writerow(header+['Property Value'])
    
    data =[]
    
    for row in csv_file_input:
    
        add = row[1]
        citystatezip= row[2]+ " "+row[3]
    
        
        get_search_results_payload = {'zws-id': zwsid, 'citystatezip':citystatezip, 'address':add}
        get_search_results_url = "http://www.zillow.com/webservice/GetSearchResults.htm"
        results = requests.get(get_search_results_url, params=get_search_results_payload)
        tree1 = html.fromstring(str(results.text))
        zpid = tree1.xpath('//zpid/text()')

        zestimate_url ="http://www.zillow.com/webservice/GetZestimate.htm"
        zestimate_payload ={'zws-id':zwsid, 'zpid':zpid}
        zestimate = requests.get(zestimate_url, params=zestimate_payload)
        tree2 = html.fromstring(str(zestimate.text))
        
        value = tree2.xpath('//amount[@currency="USD"]/text()')
        
        
        if len(value)>0:
            answer_file_object.writerow(row+value)
        else:
            answer_file_object.writerow(row+['0'])
    answer_file.close()
    


    print data


main()