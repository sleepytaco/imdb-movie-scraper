from bs4 import BeautifulSoup
import requests
import webbrowser
import sys


def main():

    imdb = 'https://www.imdb.com/'

    ##### SPACER #####
    for i in range(30):
        print()

    ##### GETTING MOVIE NAME INPUT #####
    if len(sys.argv) > 1:  # either from command line argument
        movie = ' '.join(sys.argv[1:])
    else:  # or via text input
        movie = input('Enter a movie name: ')

    ##### MAIN LOOP #####
    while movie != 'q':

        ##### SPACER #####
        for i in range(30):
            print()

        ##### IMDB SEARCH PAGE INFO #####
        site = requests.get(imdb + f'find?q={"+".join(movie.split(" "))}&ref_=nv_sr_sm')
        soup = BeautifulSoup(site.text, 'lxml')
        movie_page = soup.find_all('td', class_='result_text')[0].find_all('a')[0].get('href')
        movie_page_ref_code = movie_page.split('/')[2]  # get the movie's reference code from the search results

        ##### MOVIE PAGE INFO #####
        site = requests.get(imdb + movie_page)
        soup = BeautifulSoup(site.text, 'lxml')
        movie_name_and_year = ' '.join(soup.find_all('div', class_='title_wrapper')[0].find_all('h1')[0].text.split('\xa0'))
        try:
            metacritic_score = soup.find_all('div', class_='metacriticScore')[0].text.strip()
        except IndexError:
            metacritic_score = "N/A"
        print("Movie: ", movie_name_and_year)
        print("Metascore: ", metacritic_score)

        ##### PARENTS GUIDE PAGE INFO #####
        parents_guide_page = f'https://www.imdb.com/title/{movie_page_ref_code}/parentalguide?ref_=tt_stry_pg'
        site = requests.get(parents_guide_page)
        soup = BeautifulSoup(site.text, 'lxml')

        try:
            nudity_level = soup.find_all('section', {'id': 'advisory-nudity'})[0].find_all('li')[0].text.strip().split('\n')[0]
        except IndexError:
            webbrowser.open(parents_guide_page)
        if len(soup.find_all('section', {'id': 'advisory-nudity'})[0].find_all('li')) == 1:
            nudity = "N/A"
        else:
            nudity = nudity_level
        print("Nudity level:", nudity)

        print("Description:")
        # if no sex & nudity descriptions found
        if len(soup.find_all('section', {'id': 'advisory-nudity'})[0].find_all('li')) == 1:
            print("No description found.")
        else:
            # print out the descriptions if available
            for i in range(1, len(soup.find_all('section', {'id': 'advisory-nudity'})[0].find_all('li'))):
                print(f'{i}. ',
                      soup.find_all('section', {'id': 'advisory-nudity'})[0].find_all('li')[i].text.strip().split('\n')[
                          0])

        # in case not much information found the movie's page is opened in your web browser
        if metacritic_score == 'N/A' and nudity == 'N/A':
            webbrowser.open(imdb+movie_page)

        movie = input("\nEnter another movie name or 'q' to quit: ")

    ##### SPACER #####
    for i in range(30):
        print()
    print('Bye bye!')


main()
