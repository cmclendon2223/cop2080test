from menu import Menu 


mainMenu = Menu()

mainMenu.addOption("Check Avalible Memory")
mainMenu.addOption("View Network Connections")
mainMenu.addOption("Display Free Ram and Swap")
mainMenu.addOption("Quit")

choice = mainMenu.getInput()