//---------------------------------------------------
//         *****!Do not edit this file!*****
//---------------------------------------------------
//   ___  ___  _  __  __  __  __                   
//  | _ \|_  )(_)|  \/  ||  \/  |                  
//  |  _/ / /  _ | |\/| || |\/| |                  
//  |_|__/___|(_)|_|  |_||_|  |_|                  
//   / __| ___  __| | ___                          
//  | (__ / _ \/ _` |/ -_)                         
//  _\___|\___/\__,_|\___|     _     _           _ 
//  \ \ / /__ _  _ _ (_) __ _ | |__ | | ___  ___(_)
//   \ V // _` || '_|| |/ _` || '_ \| |/ -_)(_-< _ 
//    \_/ \__,_||_|  |_|\__,_||_.__/|_|\___|/__/(_)
//---------------------------------------------------
// Purpose: Here, we declare and set up almost
//          every variable used throughout the
//                  P2:MM codebase
//---------------------------------------------------

if (RandomPortalSize==true) {
    randomportalsize <- 34
    randomportalsizeh <- 34
}

// Setup A Global SpawnClass
GlobalSpawnClass <- class {
    // Try To Make All Spawns Global
    useautospawn = false
    // Use Set Spawnpoint
    usesetspawn = false

    // Set SpawnPoint
    setspawn = class {
        // Set SpawnPoint
        position = Vector(0,0,0)
        // Set Radius
        radius = 0
    }

    // Reds Spawn Parameters
    red = class {
        spawnpoint = Vector(0,0,0)
        rotation = Vector(0,0,0)
        velocity = Vector(0,0,0)
    }
    // Blues Spawn Parameters
    blue = class {
        spawnpoint = Vector(0,0,0)
        rotation = Vector(0,0,0)
        velocity = Vector(0,0,0)
    }
}

IsOnSingleplayer <- false
if (GetMapName().slice(0,7)=="mp_coop") {
    IsOnSingleplayer = false
} else {
    IsOnSingleplayer = true
}


OriginalAngle <- null
CanCheckAngle <- false

OriginalPosMain <- null

player1discordhookstr <- ""
CanHook <- false
Player2Joined <- false
hasbeenremoved <- false
PostMapLoadDone <- false
TickSpeed <- 0.00 // now depricated just for legacy
EventList <- []
PermaPotato <- false
TotalRemovedEnts <- 0
MadeSpawnClass <- false
usefogcontroller <- false
DevModeConfig <- DevMode
StartDevModeCheck <- false
PreviousTimeDeath <- 0
HasRanGeneralOneTime <- false
BundgeeHookID <- "none"
BundgeeHookMessage <- "none"
OrangeCacheFailed <- false
CanClearCache <- false
DoneCacheing <- false
IsInSpawnZone <- []
HasSpawned <- false
PlayerColorCached <- []
CurrentlyDead <- []
PlayerID <- 0
PreviousTime5Sec <- 0
amtoffsetclr <- 0
GBIsMultiplayer <- 0
cacheoriginalplayerposition <- 0
DoneWaiting <- false
IsSingleplayerMap <- false
PluginLoaded <- false
PreviousTime1Sec <- 0
playerclasses <- []
entityclasses <- []
fogs <- false
CurrentPythonOutputID <- 0
CurrentPythonInputID <- 0

ConsoleAscii <- [
""
"██████╗░░█████╗░██████╗░████████╗░█████╗░██╗░░░░░░░░░██████╗░"
"██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║░░░░░░░░░╚════██╗"
"██████╔╝██║░░██║██████╔╝░░░██║░░░███████║██║░░░░░░░░░░░███╔═╝"
"██╔═══╝░██║░░██║██╔══██╗░░░██║░░░██╔══██║██║░░░░░░░░░██╔══╝░░"
"██║░░░░░╚█████╔╝██║░░██║░░░██║░░░██║░░██║███████╗░░░░███████╗"
"╚═╝░░░░░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚══════╝░░░░╚══════╝"
""
"███╗░░░███╗██████╗░░░░░███╗░░░███╗░█████╗░██████╗░"
"████╗░████║██╔══██╗░░░░████╗░████║██╔══██╗██╔══██╗"
"██╔████╔██║██████╔╝░░░░██╔████╔██║██║░░██║██║░░██║"
"██║╚██╔╝██║██╔═══╝░░░░░██║╚██╔╝██║██║░░██║██║░░██║"
"██║░╚═╝░██║██║░░░░░░░░░██║░╚═╝░██║╚█████╔╝██████╔╝"
""
]

CheatsOn <- false

// Add names to credits
MPMCoopCreditNames <- [
"### ",
"### ",
"### ",
"### ",
"###Portal 2: Multiplayer Mod ~ Credits",
"### ",
"###--------------------------",
"###P2:MM Head Creators",
"###--------------------------",
"kyleraykbs | Team Lead + Scripting",
"Vista | Reverse Engineering, Plugin Developer",
"Bumpy | Script Theory",
"Wolƒe Strider Shoσter | Scripting + Singleplayer Support",
"Nanoman2525 | Mapping + Entity Work + Launcher",
"###--------------------------",
"###P2:MM Team Members",
"###--------------------------",
"cabiste | Scripting + Mod Launcher + Code Refactor",
"sear | Theorycrafting + Ideas",
"Jeffrey | Ideas",
"###--------------------------",
"###Multiplayer Mod: Contributers",
"###--------------------------",
"Darnias | Jumpstarter Code",
"actu | Remote File Downloads",
"Blub/Vecc | Code Cleanup + Commenting",
"AngelPuzzle | Translations for other langauges",
"SuperSpeed | Heavy playtesting",
"###--------------------------",
"###Special thanks to...",
"###--------------------------",
"Dreadnox",
"Slingexe",
"nintendude",
"Souper Marilogi",
"wol",
"###--------------------------",
"###Valve: Credits",
"###--------------------------",
]