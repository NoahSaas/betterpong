if not(game:IsLoaded()) then
	game.Loaded:Wait()
	game.Workspace.Characters:WaitForChild(game.Players.LocalPlayer.Name)
	print(game.Players.LocalPlayer.Name .. " spawned in")
end

_G.whitelist = {
    ["dmHUN"] = true,
    ["Trinationx"] = true,	
    ["xHemonek"] = true,
    ["LM1502"] = true,
    ["LegiBarbieQueenBunny"] = true,
    ["Redtaract"] = true,
    ["jeqcuiz"] = true,
    ["WillingAz9"] = true,        
    ["Wasili3334"] = true,        
    ["JohnBTW"] = true,        

}

_G.AutoAlly = true
local plr = game.Players.LocalPlayer
local main = plr.PlayerGui:WaitForChild("Main")
local gui = main:WaitForChild("Allies")
local Players = gui.Container.Players.ScrollingFrame.Frame
local Requests = gui.Container.Requests.ScrollingFrame.Frame
local inv = main.InventoryContainer
local crew = main.Crew
local remotes = game.ReplicatedStorage.Remotes
local signal = main.AlliesButton.Activated

for i, connection in ipairs(getconnections(main.InventoryButton.Activated)) do
   local func = connection.Function
   func()
   func()
end


local function updateAllies()
    for i, connection in ipairs(getconnections(signal)) do 
        local func = connection.Function
        if inv:GetAttribute("itemsVisible") == false and crew.Visible == false then
            func()
            func()
        end
    end
    task.wait()
end

local function CheckRequests()
    for i, v in ipairs(Requests:GetChildren()) do
        if _G.whitelist[v.Name] then
            local ally = v.Name
            remotes.CommF_:InvokeServer("AcceptAlly", ally)
            print("Accepted " .. ally .. "'s request")
        end
    end
    task.wait()
end

local function RequestAlly()
    for i, v in ipairs(Players:GetChildren()) do
        if _G.whitelist[v.Name] and not (v.Label.Text == "(Pending)") then
            local ally = v.Name
            remotes.CommF_:InvokeServer("InviteAlly", ally)
            print("Request sent to " .. ally)
        end
    end
    task.wait()
end


while true do
    if _G.AutoAlly then
        updateAllies()
        RequestAlly()
        CheckRequests()
    end
    task.wait(1)
end