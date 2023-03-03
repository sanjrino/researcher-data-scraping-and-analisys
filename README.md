# researcher-data-scraping-and-analisys
Student job at Innorenew, consisting in scraping the data of scientific papers and arranging them in an Excel, later used for analisys.

This was the first proper python program that i wrote, and this experience made me fall in love with the language. I learned to explore and give a chance to new datatypes, like dictionaries, and not to write everything with arrays, like i did while using c++. I plan on rewriting the program in the future properly, maybe using pandas and BeautifulSoup, and to try webscraping in the future.
This program is the final version I used for the job, and it was based on attempts of scraping data from a pdf and html. at the end i stuck with xml, as it ended being the most complete and easy data to work with.

The python scripts needs ResearchersAffAndCountry.csv for the researcher data, and cobiss.csv for the already present journals. A try except could be implemented, returning both of the files blank.

The main.py takes the data from the xml, splits the file into a list of categories, that is later split into single journals and saved into a dictionary with the cobiss ID as key, and category and rest of file as the values [0],[1].
Author information is generated manually with another .csv file, using the previous data as reference. As some values (IR affiliatoin) were paper dependent, I later kept only the data that doesnt vary, mainly IR author.
In the future, it could be possible to write the informations of, for example, students not employed at innorenew but with the IR affiliation, eliminating in some part the manual labour in the samll edge cases.
I later compared the values of already present cobiss id, extracted from the already present Excel. If the cobiss key  was not present, I would call the writeline function, extracting the data from the rest of the dictionary and appending a line to a .tsv file. I tried to scrape the ID of the people in the xml and compare it to the sicris ID to see if they are employed, but ofthen the code ID in the xml varies between different formats.
In the future, in case the program will be used, I suggest finding a way to generate data by scraping the cobiss website, using the .xml only for the cathegory, author and cobiss. alternatively, using google scholar to scrape the number of citations, with the title as input. The problem with that approach is that there are cases where there are multiple papers with the same title, there are no papers with that title, or another paper with a similar title is displayed.
Another problem I encountered is that the .xml files ofthen does not contain the data in a consistent way, making manual work necessary for the review.

Any comments on how my code should be changed or any tips are welcome.
