from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def run_research_popeline(topic : str) -> dict:

       state = {}

       #search agent working 
       print("\n"+" ="*50)
       print(" step 1 - search agent is working ... ")
       print("="*50)

       search_agent = build_search_agent ()
       search_result = search_agent.invoke({
            "messages" : [("user", f"find recent ,reliable and detailed information about : {topic}" )]
       })
       state["search_result"] = search_result ['messages'] [-1].text

       print("\n search_result", state ['search_result'])

       #step 2 - reader agent 
       print("\n" + "="*50)
       print(" step 2 - reader agent is scraping top resources ... ")
       print("="*50)
       reader_agent = build_reader_agent()
       reader_result = reader_agent.invoke({
              "messages":[("user",
                          f"based on the following search result about'{topic}' ,"
                          f"pick on the most relevant URL and scrape it for deeper content.\n\n"
                           f"search result:\n{state['search_result'] [:2000]}"
              )]
       })
       state['scraped_content'] = reader_result['messages'][-1].text
       print(" \n scraped content \n",state['scraped_content'])

       #step 3 - writer chain
       print("\n"+" ="*50)
       print(" step 3 - writer  is drafting the report ... ")
       print("="*50)

       research_combined = (
              f"SEARCH RESULTS : \n {state['search_result']}\n\n"
              f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"

       )

       state['report'] = writer_chain.invoke({
             "topic" : topic,
             "research" : research_combined
      }) 
      
       print("\n Final Report \n", state['report']) 
       
       
       #critic report

       print("\n"+" ="*50)
       print(" step 4 - critic is reviewing the report ... ")
       print("="*50)

       state["feedback"] =critic_chain.invoke({
              "report" : state['report']
       })

       print("\n critic report \n", state['feedback'])
       return state


if __name__ == "__main__":
     topic = input("Enter a research topic: ")
     run_research_popeline(topic)