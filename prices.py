import currency
import requests, json, time, datetime, csv


def timestamp_to_str(ts):
    return datetime.date.fromtimestamp(ts).strftime('%m/%d/%Y')


def main():

    start = datetime.date.today() - datetime.timedelta(2)
    end = datetime.date.today()

    days = int((end - start).days)

    f = []
    #read the file so that you don't have to redownload
    with open('market_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            f.append(row)



    for i in range(days):

        ts =  int(time.mktime((start + datetime.timedelta(days=i)).timetuple()))
        print("Fetching day: " + )
        #check to see if this date has allready been don, this is a dirty solution to loop theough the ordered array but it shouldn't take up too much time
        date_str =  timestamp_to_str(ts)
        for row in f:
            if row['date'] == date_str:
                break
        else:
            f.append(get_data(ts))

    if(len(f) == 0):
        return

    with open('market_data.csv', 'w') as csvfile:
        fields = [k for k in f[0]]
        writer = csv.DictWriter(csvfile, fields)

        writer.writeheader()
        for row in f:
            writer.writerow(row)




def get_data(timestamp):
    d = {}
    d['date'] = datetime.date.fromtimestamp(timestamp).strftime('%m/%d/%Y')
    for curr, a in currency.pairs.items():
        #cryptocompare can only have 5 items in the request, bloody inconvinent
        for i in range(int(len(a) / 5) + 1):
            keys = []
            if (i + 1) * 5 >= len(a):
                keys = a[i*5:]
            else:
                keys = a[i * 5 : (i + 1) * 5]

            r = ''

            for key in keys:
                r += key + ','

            comma_key_set = r[:-1]

            data = json.loads(requests.get('https://min-api.cryptocompare.com/data/pricehistorical?fsym=' + curr + '&tsyms=' + comma_key_set + '&ts=' + str(timestamp)).text)[curr]
            for key, price in data.items():
                d[curr + '_' + key] = price

    return d

if __name__ == '__main__':
    main()
