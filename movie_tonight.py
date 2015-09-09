__author__ = 'vivek'

import requests
import json
from os import walk
import matplotlib.pyplot as mp
import concurrent.futures
import sys
from string import digits
import csv

   

def get_movie_info(name):
    # name = raw_input("Enter movie name")

    URL_IMDB = "http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q="
    URL_OMDB = "http://www.omdbapi.com/?plot=short&r=json&i="
    header_ = {"User-Agent": "console(imdb.py)",}

    try:
        resp = requests.get(URL_IMDB + name, headers=header_)
    except:
        return -11 

    try:
        json_response = json.loads(resp.text)
        # print json_response

        if json_response.has_key("title_popular"):
            title_substring = json_response["title_popular"]
        else:
            title_substring = json_response["title_approx"]

        item = title_substring[0]
        mid = item.get("id")
        mname = item.get("title")

        # print mid, mname
        try:
            omdb_resp = requests.get(URL_OMDB + mid)
        except:
            return -11 

        try:
            
            json_omdb = json.loads(omdb_resp.text)


            # print json_omdb
            year = json_omdb["Year"]
            plot = json_omdb["Plot"]
            imdbRating = json_omdb["imdbRating"]
            imdbVotes = json_omdb["imdbVotes"]
            name = json_omdb["Title"]
            metaScore=json_omdb["Metascore"]
            genre=json_omdb["Genre"]
            director=json_omdb["Director"]
            print name.upper()," -" , imdbRating,"(",year,"):",plot,"\n"

            fcsv = csv.writer(open("imdb.csv", "ab+"))
            fcsv.writerow([name, imdbRating,imdbVotes, year, plot,metaScore,genre,director])            

            return imdbRating
        except (ValueError, KeyError, TypeError):
            print "Loading"

    # print(decoded["title_approx"])
    except (ValueError, KeyError, TypeError):
        print "loading"

    return None


def get_movie_list(path):
    """ Gets the list of all files and folder in the pwd(or path)"""
    file = []
    for (dirpath, dirnames, filenames) in walk(path):
        file.extend(filenames)
        file.extend(dirnames)
        break


    # Cleaning Out the data
    for idx in range(len(file)):
        #print movie
        file[idx] = file[idx].replace(".", " ")  #remove "."
        file[idx] = file[idx].translate(None, digits)  #strip years
        file[idx] = file[idx].replace("()", " ")  #remove "()"
        file[idx] = file[idx].replace("mkv", " ")  #remove "mkv"
        file[idx] = file[idx].replace("avi", " ")  #remove "avi"
        file[idx] = file[idx].replace("mp", " ")  #remove "mp4"
        file[idx] = file[idx].replace("DVDRip", " ")  #remove "DVDRip"

    #print_movie_list(file)

    return file


def print_movie_list(movie_list):
    """Prints Movie list """

    for f in movie_list:
        print f


def plot_movie_info(x, y, movie_name_list):
    """Plots Movies agains there ratings"""
    mp.plot(x, y, 'ro')
    mp.ylabel("IMDB Rating")
    mp.xlabel("Movies ")
    # mp.xticks(x, movie_name_list)
    mp.ylim(ymin=0, ymax=10)

    for i in range(len(y)):
        mp.annotate(str(movie_name_list[i])[0:15] + "(" + str(y[i]) + ")", xy=( x[i], y[i]), xytext=(x[i], y[i]),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    )
    mp.savefig('results.png', bbox_inches='tight')


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print("This program requires at least one parameter")
        sys.exit(1)

    path = sys.argv[1]
    

    if path[0]=="/":      #If path exist 

        str(path).replace(" ", " \\")
        #print path    

        y = []
        movie_list = get_movie_list(path)

        executor = concurrent.futures.ProcessPoolExecutor(10)
        futures = [executor.submit(get_movie_info, movie_name) for movie_name in movie_list]
        concurrent.futures.wait(futures)

        for j in futures:
            yVal = j.result()

            if yVal==-11 :
                print "Connection Error"
                break

            if (str(yVal) == 'N/A') or (yVal == None):
                yVal = 0

            y.append(yVal)

        # print y
        x = range(len(y))
        plot_movie_info(x, y, movie_list)


    else:   #else if argument passed via shell script($1,movie name==path)
        get_movie_info(path)
