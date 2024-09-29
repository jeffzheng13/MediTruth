import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json

topic_prompt = """
        You are tasked with taking a JSON input with multiple research papers data and a question regarding the information in the data, then returning if the question I gave to you was true or false. If you can not conclude anything with the question, you must return value as 'inconclusive'. Otherwise, return value as 'true' or 'false' with a description as a summary of why it is true or false, title as article title, and similarity as the second value in Document. The output should be in JSON format, with key-value pairs that look like this: 
        {{
            'value': '',
            'description': '',
            'title': '',
            'similarity': ''
        }}

        Your input will be a JSON object with the following format where your reasearch paper data for each document is in the page_content field:
        [(Document(
                metadata={{
                        '_id': '', 
                        'uid': '', 
                        'Title': '.', 
                        'Published': '--', 
                        'Copyright Information': ''}}, 
                page_content=''), 
                0.7651486992835999), 
        ................

        (Document(
                metadata={{
                        '_id': '', 
                        'uid': '', 
                        'Title': '.', 
                        'Published': '--', 
                        'Copyright Information': ''}}, 
                page_content=''), 
                0.7651486992835999), 
        ]
        
        The research data is:
        {data}

        The question is:
        {question}
    """


safety_settings = {
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE
}

def fact_check(research_data, question, temperature=0):
    # 2. setup gemini and prompt
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 3. generate facts
    facts_response = model.generate_content(
        topic_prompt.format(data=research_data, question=question),
        generation_config={"temperature": temperature},
        safety_settings=safety_settings)
        
    # 4. clean up response
    start = facts_response.text.find('{')
    end = facts_response.text.rfind('}')
    if start == -1 or end == -1:
        raise Exception("Invalid response from model: " + facts_response.text)
    cleaned_facts_response = facts_response.text[start:end+1]

    # 5. return response
    facts_dict = json.loads(cleaned_facts_response)
    return facts_dict



# data = fact_check(
#     research_data="[(Document(metadata={'_id': 'a571df3f-0c17-4817-8d34-67e136f84018', 'uid': '19744178', 'Title': 'Growth rate of human fingernails and toenails in healthy American young adults.', 'Published': '2009-09-08', 'Copyright Information': ''}, page_content='BACKGROUND: Human nail clippings are increasingly used in epidemiological studies as biomarkers for assessing diet and environmental exposure to trace elements or other chemical compounds. However, little is known about the growth rate of human nails.\nOBJECTIVE: To estimate the average growth rate of fingernails and toenails and examine factors that may influence nail growth rate.\nMETHODS: Twenty-two healthy American young adults marked their nails close to the proximal nail fold with a provided nail file following a standardized protocol, and recorded the date and the distance from the proximal nail fold to the mark. One to three months later, participants recorded the date and distance from the proximal nail fold to the mark again. Nail growth rate was calculated based on recorded distance and time between the two measurements.\nRESULTS: Average fingernail growth rate was faster than that of toenails (3.47 vs. 1.62 mm/month, P < 0.01). There was no significant difference between right and left fingernail/toenail growth rates. The little fingernail grew slower than other fingernails (P < 0.01); the great toenail grew faster than other toenails (P < 0.01). Younger age, male gender, and onychophagia were associated with faster nail growth rate; however, the differences were not statistically significant.\nCONCLUSION: Nail growth rates have increased compared with previous estimates conducted decades ago. Toenail clippings may reflect a long exposure time frame given the relatively slow growth rate.'), 0.8736217617988586), (Document(metadata={'_id': 'bb5f1379-6bc0-4853-b2e1-fc56e8901861', 'uid': '24079589', 'Title': 'Longitudinal melanonychias.', 'Published': '--', 'Copyright Information': '© 2013 Elsevier Inc. All rights reserved.'}, page_content='Melanonychia is black or brown pigmentation that appears in the fingernails and toenails. The pigment can come from exogenous sources, such as bacteria or fungal infection, tar, or blood. Endogenous causes include aberrant melanin production in the nail bed, resulting in a longitudinal presentation. Melanonychia can indicate the presence of cancerous growths, as well as infection. Diagnostic measures, including dermatoscopy, biopsy, and histopathology, can determine the cause and direct the course of treatment. Malignant lesions should be excised, and underlying infections should be addressed with antibiotics or antifungals. Benign lesions and hyperpigmentation may benefit from a wait-and-see approach.'), 0.7651486992835999), (Document(metadata={'_id': '868288e9-6d4d-476c-9f0f-d816652703df', 'uid': 'PMC6244569', 'Title': 'Toxic Side Effects of Targeted Therapies and Immunotherapies Affecting the Skin, Oral Mucosa, Hair, and Nails', 'Published': '2018-10-30', 'Copyright Information': ''}, page_content='Cutaneous toxicities of targeted therapies and immunotherapies profoundly diminish patient QoL, and impairment appears to be unexpectedly more severe in patients treated with a targeted therapy than with chemotherapy (total score 41.7 vs. 32.8; \u2009=\u20090.02) []. The emotional component is the most significantly affected domain (50.0 vs. 38.1; \u2009=\u20090.02), followed by symptoms and pain, indicating that patients experience a sense of loss of privacy due to their inability to hide their cancer. The management of skin toxicities is therefore critical to improving cancer patient outcomes. However, compared with dermatologists, oncologists more often overestimate the severity of dermatologic adverse events (dAEs) [] and are more prone to discontinuing cancer therapy as a result of skin toxicities, hence reducing patient access to a potential life-saving treatment. An interdisciplinary collaborative approach between dermatologists and oncologists is therefore essential to caring for patients receiving anticancer therapies. Immune checkpoints have a critical role in maintaining normal immunologic homeostasis by downregulating T\xa0cell activation. Therapeutic blockade of cytotoxic T\xa0lymphocyte-associated antigen\xa04 (CTLA-4)/programmed death-1 (PD-1) receptors or PD-ligand 1 (PD-L1) leads to constitutive CD4\u2009+/CD8\u2009+\u2009T\xa0cell activation, shifting the immune system toward antitumor activity []. Because of this unique mechanism of action, ICIs have a specific safety profile referred to as immune-related adverse events (irAEs) which affect virtually all organs in the body []. Cutaneous toxicities are the most frequent irAEs, affecting 40% of patients []; they occur within the first 4–8\xa0weeks and can be long-lasting. A non-specific  is most commonly reported (Fig.\xa0), with a frequency ranging from 14 to 40% depending on the drug and whether it is used in combination or alone []. Subsets of patients also present eczema-like or psoriatic lesions [] while others develop lichenoid dermatitis [, ] in response to PD-1 and PD-L1 inhibitors. Lichenoid rash in patients treated with ICIs is very similar to idiopathic lichen planus, except for a slightly increased abundance of CD163-positive cells indicating a macrophage–monocyte lineage []. Other bothersome irAEs include xerosis and pruritus with secondary excoriations, which may be associated with a rash. Although all-grade pruritus is frequent (10–30% of patients) [, ], it remains underreported and underdiagnosed. As this irAE has a profound negative impact on patients’ QoL, it is currently the focus of intense investigation. Treatment includes high-potency corticosteroids or γ-aminobutyric acid (GABA) agonists along with antihistamines for grade\u2009≥\u20092 toxicities. Other clinical presentations of irAEs include autoimmune bullous disorders such as BP180/230-positive bullous pemphigoid (BP) [] in\u2009<\u20091% of patients, as well as worsening or de novo appearance of autoimmune dermatosis such as psoriasis []. Rarely, life-threatening conditions such as grade\xa04 Stevens-Johnson syndrome (SJS)-like eruptions may develop; these warrant prompt recognition, discontinuation of treatment, and aggressive management []. Vitiligo is also commonly described in patients treated for melanoma [, ]. Patients are usually not bothered by the disease as its impact on their social life is minor. Interestingly, however, patients who develop cutaneous reactions in response to pembrolizumab [, ] or rash or vitiligo when treated with nivolumab [] have an overall increased survival and better outcomes than those who do not, suggesting a better response to immunotherapy. ICI-treated patients must therefore receive proper counselling as part of a supportive care regimen to help them cope with dermatological toxicities and ensure that QoL is maintained. Targeted therapies may cause damage to nail folds, with paronychia and periungual pyogenic granuloma distinct from chemotherapy-induced lesions (Fig.\xa0a, b) that are mostly observed in the nail plate or the nail matrix. As some patients may receive both treatment types combined, clinicians must be fully informed of differences between chemotherapy and targeted therapy-associated nail toxicities. Paronychia and periungual granulomas are mostly reported in response to EGFRIs, with a 17.2% all-grade toxicity incidence [], as well as MEKIs and mTOR inhibitors to a lesser extent []. Typical lesions, which mostly affect toenails or thumbs, develop slowly after several weeks or months of treatment. Damage typically starts with the development of periungual inflammatory paronychia and can evolve into overgrowing of friable granulation tissue on lateral and/or proximal nail folds, mimicking ingrown nails. Although usually not severe, such lesions can still be very debilitating for the patient, especially when they persist for a long time. Therefore, aggressive strategies must be implemented to help patients cope with these adverse effects. The standard of care for pyogenic granuloma is surgery with partial removal of the nail plate and matrix and physical destruction of the granulation tissue and phenolization []. In patients with multiple concomitant lesions, conservative treatment should be prioritized, with supportive oncodermatology while maintaining targeted therapy. In close collaboration with a podiatrist, nail curvature can be corrected if needed. Stretchable tape, liquid nitrogen, a combination of topical corticosteroids and antibiotics, antiseptic soaks, and silver nitrate can also be used []. Topical timolol can also be helpful for periungual pyogenic granuloma []. Patients treated with MEKIs, EGFRIs, and mTOR inhibitors can also develop mild to moderate changes of the nail bed and matrix. These lesions are characterized by mild onycholysis, brittle nails, and a slower nail growth rate []. Selective pan-FGFR\xa01–4 inhibitors are a new class of targeted therapy drugs currently under development for a large range of solid tumors. More than 35% of patients receiving these drugs experience very severe nail toxicities 1–2\xa0months after starting the treatment, with onycholysis, onychomadesis, and nail bed superinfection occurring []. These dose-dependent adverse events are similar to taxane-related nail changes. Ibrutinib is a first-in-class, oral covalent inhibitor of Bruton’s tyrosine kinase that is now approved in chronic lymphocytic leukemia and cell mantle lymphoma. Nail changes including brittle nails (23–67% of patients), onychoschizia, onychorrhexis, and onycholysis have been described. These nail changes become apparent after several months of treatment (median 6–9\xa0months) and are commonly associated with hair changes [].'), 0.7166118621826172)]",
#     question="Do cutaneous toxicities of targeted therapies benefit patient?",
#     gemini_key=os.getenv("GEMINI_KEY"),
#     temperature=0
# )


# print(data)