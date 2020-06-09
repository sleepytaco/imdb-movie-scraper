from bs4 import BeautifulSoup
import requests
import webbrowser
import sys


def main(movie=''):

    imdb = 'https://www.imdb.com/'

    ##### SPACER #####
    for i in range(30):
        print()

    ##### GETTING MOVIE NAME INPUT #####
    if movie == '':
        if len(sys.argv) > 1:  # either from command line argument
            movie = ' '.join(sys.argv[1:])
        else:  # or via text input
            movie = input('Enter a movie name or \'q\' to quit: ')

    ##### MAIN LOOP #####
    while movie != 'q':

        ##### SPACER #####
        for i in range(30):
            print()

        ##### IMDB SEARCH PAGE INFO #####
        site = requests.get(imdb + f'find?q={"+".join(movie.split(" "))}&ref_=nv_sr_sm')
        soup = BeautifulSoup(site.text, 'lxml')
        try:
            movie_page = soup.find_all('td', class_='result_text')[0].find_all('a')[0].get('href')
        except IndexError:
            print(f"Uh-oh! No such movie called '{movie}' was found!\n")
            g = input(f"Enter 1 to google '{movie}' or type another movie to search: ")
            if int(g) == 1:
                webbrowser.open(f'https://www.google.com/search?q={"+".join(movie.split(" "))}+movie')
                ##### SPACER #####
                for i in range(30):
                    print()
                movie = input('Enter a movie name or \'q\' to quit: ')
                continue
            movie = g
            continue
        movie_page_ref_code = movie_page.split('/')[2]  # get the movie's reference code from the search results

        ##### MOVIE PAGE INFO #####
        site = requests.get(imdb + movie_page)
        soup = BeautifulSoup(site.text, 'lxml')
        try:
            movie_name_and_year = ' '.join(soup.find_all('div', class_='title_wrapper')[0].find_all('h1')[0].text.split('\xa0'))
        except IndexError:
            open_page = input(f"Looks like not much information about the movie was found!\nEnter '1' to google '{movie}' or '2' to search again: ")

            # input validation
            if open_page in ['1', '2']:
                if open_page == '1':
                    webbrowser.open(f'https://www.google.com/search?q={"+".join(movie.split(" "))}+movie')
                elif open_page == '2':
                    movie = input('Enter a movie name or \'q\' to quit: ')
                    main(movie)
            else:
                while open_page not in ['1', '2']:
                    open_page = input("Type in either '1' or '2': ")
                    if open_page == '1':
                        webbrowser.open(f'https://www.google.com/search?q={"+".join(movie.split(" "))}+movie')
                    elif open_page == '2':
                        movie = input('Enter a movie name or \'q\' to quit: ')
                        main(movie)
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
            nudity_level = "N/A"
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

        # in case not much information found the option to open movie's page in your web browser is prompted
        if metacritic_score == 'N/A' and nudity == 'N/A':
            open_page = input("\nUh-oh! Looks like not much information about the movie was found!\nEnter '1' to google the movie or '2' to search again: ")

            # input validation
            if open_page in ['1', '2']:
                if open_page == '1':
                    webbrowser.open(f'https://www.google.com/search?q={"+".join(movie.split(" "))}+movie')
            else:
                while open_page not in ['1', '2']:
                    open_page = input("Type in either '1' or '2': ")
                    if open_page == '1':
                        webbrowser.open(f'https://www.google.com/search?q={"+".join(movie.split(" "))}+movie')

        movie = input("\nEnter another movie name or 'q' to quit: ")

    ##### SPACER #####
    for i in range(30):
        print()
    print('Bye bye!')
    sys.exit()


main()
