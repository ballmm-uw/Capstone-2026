#LIS 572 - Final Project — Computational Analysis/Data Visualizations
#Rowan Tabor

#load in excel sheet, don't need stringsAsFactors arg for this function.
install.packages("readxl")
library(readxl)
oral_histories<-read_excel("/Users/rowantabor/Desktop/capstone/NER_set_final/plain_text/Book1.xlsx")


#install and load packages
install.packages("tidytext")
install.packages("tidyverse")
library(tidytext)
library(tidyverse)
library(dplyr)
library(stringr)

#check df
nrow(oral_histories)



#1 INTERVIEWS PER YEAR

#add year as it's own column. when trying to plot this later, using the scale_x_continuous function, i learned that the years were being treated as characters. calling the as.numeric function in the original modification keeps me from needing to call it in the aes() function every time i make visualizations with these values.
oral_histories_w_year <- oral_histories %>%
  mutate(clean_year = as.numeric(str_extract(field_interview_date, "\\d{4}")))

#count by year
interviews_per_year <- oral_histories_w_year %>%
  group_by(clean_year) %>%
  summarise(num_interviews = n())

#plot!
ggplot(data = interviews_per_year) +
  geom_line(mapping = aes(x = clean_year, y = num_interviews, group = 1)) +
  labs(title = "AIP Oral Histories by Year", subtitle = "1959-2024", x = "Year", y = "Number of Interviews")



#2 TOPICS BY DECADE

#turn years into decades - adapted from SPL Regex exercise
decades <- oral_histories_w_year %>%
  mutate(
    decade = case_when(
      str_detect(clean_year, "^195.$") ~ 1950,
      str_detect(clean_year, "^196.$") ~ 1960,
      str_detect(clean_year, "^197.$") ~ 1970,
      str_detect(clean_year, "^198.$") ~ 1980,
      str_detect(clean_year, "^199.$") ~ 1990,
      str_detect(clean_year, "^200.$") ~ 2000,
      str_detect(clean_year, "^201.$") ~ 2010,
      str_detect(clean_year, "^202.$") ~ 2020))

#adapted from unnest_tokens documentation - split at comma to keep subject terms together i.e. "nuclear physics" vs "nuclear" and "physics"
topic_text <- decades %>%
  unnest_tokens(word, field_subjects, token = stringr::str_split, pattern = ", ") %>% 
  filter(nchar(word) > 0)

#count the topics, include decades, filter out blank values
topic_count <- topic_text %>%
  count(word, decade, sort = TRUE) %>% 
  filter(nchar(word) > 0)

#change the name of the count column because i ran into problems trying to run max(n) later
topic_count <- topic_count %>% rename_at('n', ~'count')

#filter for the top count of each decade
topic_by_decade <- topic_count %>% 
  group_by(decade) %>%
  filter(count == max(count))

#plot!
ggplot(data = topic_by_decade) +
  geom_col(mapping = aes(x = decade, y = count, fill = word)) +
  labs(title = "Top Indexing Terms by Decade", subtitle = "In AIP Oral Histories 1959-2024", x = "Decade", y = "Number of Instances", fill = "Term") +
  scale_color_brewer(palette = "Set1")



#3 TF-IDF

#split into single words
oral_history_text<- oral_histories_w_year %>%
  unnest_tokens(word, body)

#check df
nrow(oral_history_text) #8524169

#stopwords
install.packages("stopwords")
library("stopwords")

en_stopwords <- data.frame(word = stopwords(language = "en", source = "snowball"))

#remove stopwords
oral_history_text_no_stops <- oral_history_text %>% 
  anti_join(en_stopwords)

#calculate tf-idf for each word. filter out words with negative values.
subject_tf_idf <- oral_history_text_no_stops %>%
  anti_join(en_stopwords, by = "word") %>%
  count(title, word, sort = TRUE) %>%               
  bind_tf_idf(term = word, document = title, n) %>%
  filter(tf_idf > 0)

#select for a chosen speaker
speaker_tf_idf <- subject_tf_idf %>%
  filter(title == "Linus Pauling")

#visualization - adapted from https://www.tidytextmining.com/tfidf
library(forcats)

speaker_tf_idf %>%
  group_by(title) %>%
  slice_max(tf_idf, n = 15) %>%
  ungroup() %>%
  ggplot(aes(tf_idf, fct_reorder(word, tf_idf), fill = title)) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~title, ncol = 2, scales = "free") +
  labs(x = "tf-idf", y = NULL)
