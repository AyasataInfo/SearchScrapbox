## About
This plugin can be used with FlowLauncher.  
It allows you to search or create a page in project created with Scrapbox (https://scrapbox.io/).  
It was developed to provide quick access to a desired page immediately by eliminating the process of operating the web browser as much as possible.  
  
## Applying  
After installing FlowLauncher, apply the plugin using the following steps.  (assuming it is installed on C drive)  
  
1. Navigate to C:\Users\\[UserName]\AppData\Roaming\FlowLauncher\Plugins  
2. Create a new folder as "SearchScrapbox".  
3. Put all files into the created folder.  
4. After moving to the folder created in the command prompt (using "cd" command), execute the following command.  
> pip install -r requirements.txt -t ./lib  
- If you can't use the pip command, please install pip command.  
5. Start FlowLauncher, type the command below and press Enter.
> Reload Plugin Data  
  
## How to use  
### Display pages within the project.  
> ss [ProjectName]  
- Up to 50 items can be displayed.
  
### Search for pages within a project.  
> ss [ProjectName] [SearchWord]
- If the page is not displayed, you can create a new page with the specified name.
  
## Note  
This plugin is not officially provided by Scrapbox. Please do not inquire about this plugin officially.
