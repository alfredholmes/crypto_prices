import currency
import requests, json, time, datetime, csv


def timestamp_to_str(ts):
    return datetime.date.fromtimestamp(ts).strftime('%Y.%m.%d')


def main():

    start = datetime.date.today() - datetime.timedelta(3)
    end = datetime.date.today()

    days = int((end - start).days)

    f = []
    #read the file so that you don't have to redownload
    try:
        with open('market_data.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                f.append(row)
    except:
        pass #should only fail if



    for i in range(days):

        ts =  int(time.mktime((start + datetime.timedelta(days=i)).timetuple()))
        print("Fetching day: " + timestamp_to_str(ts))
        #check to see if this date has allready been don, this is a dirty solution to loop theough the ordered array but it shouldn't take up too much time
        date_str =  timestamp_to_str(ts)
        for row in f:
            if row['Date'] == date_str:
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
    d['Date'] = timestamp_to_str(timestamp)
    for curr, a in currency.pairs.items():
        size = 6
        #cryptocompare can only have 6 items in the request, bloody inconvinent
        for i in range(int(len(a) / size) + 1):
            keys = []
            if (i + 1) * size >= len(a):
                keys = a[i*size:]
            else:
                keys = a[i * size : (i + 1) * size]

            r = ''

            for key in keys:
                r += key + ','

            comma_key_set = r[:-1]

            data = json.loads(requests.get('https://min-api.cryptocompare.com/data/pricehistorical?fsym=' + curr + '&tsyms=' + comma_key_set + '&ts=' + str(timestamp)).text)[curr]
            for key, price in data.items():
                if price != 0:
                    d[curr + '_' + key] = price**-1
                else:
                    print('Error, 0 returned from cryptocompare with pair: ' + curr + "_" + key + ', this means that this coin is not tracked')
    return d

if __name__ == '__main__':
    main()
