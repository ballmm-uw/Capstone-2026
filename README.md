
In collaboration with the UW Lab for Computing Cultural Heritage, professor Ben Lee, and American Institute of Physics Chief Research Officer Trevor Owens, our MLIS capstone project explored the application of artificial intelligence and other natural language processing tools to the AIP Oral History collection in order to evaluate these tools potential for use for metadata creation, analysis, validation, and description. Our project concluded by using this experience to develop crowdsourcing tools that incorporate programatic methods to identify and improve public descriptions of AIP Oral History subjects.

Our final deliverables for the project can be broken down into three sections:

1. Codebase:

We have created several python scripts to programmatically interact with the AIP Oral History collection.  Specifically, these scripts parse the raw transcript data taken directly from the AIP CMS into individual JSON files, perform named entity recognition on each of these individual files using  the spaCy natural language processing model, and then query the Wikipedia API to determine if the interview subject has an extant Wikipedia page. Each one of these scripts is discreet and produces its own set of file outputs.

2. Datasets

Two primary datasets have been compiled. The first resulting as the summation of identified entities using the spaCy model. This set consists of summaries for each interview that includes identified entities, the category of entity,  a count of how many times they appear, and three context snippets displaying a portion of the entity being used in the original interview.

Second, is a csv file containing the full-text data and metadata for each transcript. Each subject represents a row, with columns holding each metadata field from the original CMS export, such as indexing terms, abstract text, interview text, location of the interview, etc… This dataset is extremely valuable for traditional data science applications and textual analysis. Several R scripts and data visualizations were created to demonstrate this potential and are included in this repository along with a short narrative introducing the dataset.

The datasets themselves will be handed off directly to AIP and are not in this repository.

3. Applications

Our primary deliverable has been to create an Wikipedia Edit-a-thon Web App. Our earlier experience testing validation  using  LLM chatbots led us to develop an application that incorporates human feedback to identify and record AIP Oral History subjects to prioritize  in regularly held AIP Wikipedia Edit-a-thons.  We created a  working UI prototype  of the Companion App in HTML code and connected it with a free-to-use database manager Supabase.

We also have prototype code to that incorporates NER data to create an interactive network visualization of the oral history subjects. This was purely experimental and is not fully functional however could be the basis of further development.
