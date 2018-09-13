from configparser import ConfigParser

cfg = ConfigParser()
cfgr = ConfigParser()

cfg['links'] = {}
cfg['links']['link1'] = 'https://en.wikipedia.org/wiki/Asset_management'
cfg['links']['link2'] = 'https://en.wikipedia.org/wiki/Brand_management'
cfg['links']['link3'] = 'https://en.wikipedia.org/wiki/Business_intelligence'
cfg['links']['link4'] = 'https://en.wikipedia.org/wiki/Capacity_management'
cfg['links']['link5'] = 'https://en.wikipedia.org/wiki/Change_management'
cfg['links']['link6'] = 'https://en.wikipedia.org/wiki/Innovation_management'
cfg['links']['link7'] = 'https://en.wikipedia.org/wiki/Commercial_management'
cfg['links']['link8'] = 'https://en.wikipedia.org/wiki/Marketing_management'
cfg['links']['link9'] = 'https://en.wikipedia.org/wiki/Communications_management'
cfg['links']['link10'] = 'https://en.wikipedia.org/wiki/Configuration_management'
cfg['links']['link11'] = 'https://en.wikipedia.org/wiki/Conflict_management'
cfg['links']['link12'] = 'https://en.wikipedia.org/wiki/Content_management'
cfg['links']['link13'] = 'https://en.wikipedia.org/wiki/Customer_relationship_management'
cfg['links']['link14'] = 'https://en.wikipedia.org/wiki/Distributed_management'
cfg['links']['link15'] = 'https://en.wikipedia.org/wiki/Earned_value_management'
cfg['links']['link16'] = 'https://en.wikipedia.org/wiki/Electronic_business'
cfg['links']['link17'] = 'https://en.wikipedia.org/wiki/Enterprise_resource_planning'
cfg['links']['link18'] = 'https://en.wikipedia.org/wiki/Management_information_system'
cfg['links']['link19'] = 'https://en.wikipedia.org/wiki/Financial_management'
cfg['links']['link20'] = 'https://en.wikipedia.org/wiki/Human_resource_management'
cfg['links']['link21'] = 'https://en.wikipedia.org/wiki/Human_resources'
cfg['links']['link22'] = 'https://en.wikipedia.org/wiki/Incident_management'
cfg['links']['link23'] = 'https://en.wikipedia.org/wiki/Integrated_management'
cfg['links']['link24'] = 'https://en.wikipedia.org/wiki/Knowledge_management'
cfg['links']['link25'] = 'https://en.wikipedia.org/wiki/Materials_management'
cfg['links']['link26'] = 'https://en.wikipedia.org/wiki/Network_management'
cfg['links']['link27'] = 'https://en.wikipedia.org/wiki/Network_administrator'
cfg['links']['link28'] = 'https://en.wikipedia.org/wiki/Operations_management'
cfg['links']['link29'] = 'https://en.wikipedia.org/wiki/Operations_management_for_services'
cfg['links']['link30'] = 'https://en.wikipedia.org/wiki/Performance_management'
cfg['links']['link31'] = 'https://en.wikipedia.org/wiki/Power_management'
cfg['links']['link32'] = 'https://en.wikipedia.org/wiki/Problem_management'
cfg['links']['link33'] = 'https://en.wikipedia.org/wiki/Business_process_management'
cfg['links']['link34'] = 'https://en.wikipedia.org/wiki/Product_lifecycle'
cfg['links']['link35'] = 'https://en.wikipedia.org/wiki/Product_management'
cfg['links']['link36'] = 'https://en.wikipedia.org/wiki/Project_management'
cfg['links']['link37'] = 'https://en.wikipedia.org/wiki/Quality_management'
cfg['links']['link38'] = 'https://en.wikipedia.org/wiki/Records_management'
cfg['links']['link39'] = 'https://en.wikipedia.org/wiki/Resource_management'
cfg['links']['link40'] = 'https://en.wikipedia.org/wiki/Risk_management'
cfg['links']['link41'] = 'https://en.wikipedia.org/wiki/Crisis_management'
cfg['links']['link42'] = 'https://en.wikipedia.org/wiki/Sales_management'
cfg['links']['link43'] = 'https://en.wikipedia.org/wiki/Security_management'
cfg['links']['link44'] = 'https://en.wikipedia.org/wiki/Service_management'
cfg['links']['link45'] = 'https://en.wikipedia.org/wiki/Strategic_management'
cfg['links']['link46'] = 'https://en.wikipedia.org/wiki/Supply_chain_management'
cfg['links']['link47'] = 'https://en.wikipedia.org/wiki/Systems_management'
cfg['links']['link48'] = 'https://en.wikipedia.org/wiki/System_administrator'
cfg['links']['link49'] = 'https://en.wikipedia.org/wiki/Talent_management'
cfg['links']['link50'] = 'https://en.wikipedia.org/wiki/Technology_management'

#with open('static/config.ini', 'w') as configfile:
#    cfg.write(configfile)

cfgr.read('static/config.ini')

for i in range(1, 50, 1):
    linkstr = 'link'+str(i)
    link = cfgr.get('links', linkstr)
    print(link)


