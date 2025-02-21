-- Decompiled using luadec 2.2 rev:  for Lua 5.1 from https://github.com/viruscamp/luadec
-- Command line: ./system_actions.lua 

-- params : ...
-- function num : 0
module("com.teamf1.core.system.actions", package.seeall)
require("teamf1lualib/db")
require("teamf1lualib/util")
require("teamf1lualib/validations")
require("teamf1lualib/returnCodes")
require("teamf1lualib/platform_returnCodes")
require("teamf1lualib/config")
local l_0_0 = require("com.teamf1.core.returnCodes")
local l_0_1 = require("com.teamf1.core.validations")
local l_0_2 = require("com.teamf1.core.platform.returnCodes")
local l_0_3 = "system"
local l_0_4 = "reboot"
local l_0_5 = "environment"
local l_0_6 = "unitInfo"
adaptos = {}
local l_0_7 = {}
l_0_7.key = "_ROWID_"
l_0_7.keyValue = "1"
l_0_7.name = "name"
l_0_7.modelId = "modelId"
l_0_7.reboot = "reboot"
l_0_7.rebootTime = "rebootTime"
l_0_7.factoryReset = "factoryReset"
l_0_7.backupConfig = "backupConfig"
l_0_7.restoreConfig = "restoreConfig"
l_0_7.restoreConfigFile = "restoreConfigFile"
l_0_7.flashCFGPartition = "FLASH_CFG_PARTITION"
l_0_7.bootupTime = "value"
local l_0_8 = "0"
local l_0_9 = "1"
local l_0_10 = "0"
local l_0_11 = "BOOTUP_TIME"
if PRODUCT_ID == "DSR-1000AC_A1" or PRODUCT_ID == "DSR-500AC_A1" or PRODUCT_ID == "DSR-1000_B1" or PRODUCT_ID == "DSR-500_B1" then
  local l_0_12 = "10"
else
  l_0_12 = "5"
end
l_0_12 = "/tmp/"
TMP = l_0_12
l_0_12 = "backup"
BACKUP = l_0_12
l_0_12 = "flash/tmp/teamf1.cfg.ascii"
ASCII = l_0_12
l_0_12 = "flash/tmp/startup-config"
STARTUP = l_0_12
l_0_12 = "/data/tmp/factoryResetEnable"
FACTORY_RESET_ENABLE = l_0_12
l_0_12 = function()
  -- function num : 0_0 , upvalues : l_0_4, l_0_7, l_0_0
  local l_1_0 = (db.getAttribute)(l_0_4, l_0_7.key, l_0_7.keyValue, l_0_7.reboot)
  if l_1_0 == l_0_0.NIL then
    return l_0_0.FAILURE
  end
  return l_0_0.SUCCESS, 1, l_1_0
end

rebootGet = l_0_12
l_0_12 = function(l_2_0)
  -- function num : 0_1 , upvalues : l_0_0
  return l_0_0.NOT_SUPPORTED, l_2_0
end

rebootGetNext = l_0_12
l_0_12 = function(l_3_0, l_3_1)
  -- function num : 0_2 , upvalues : l_0_0, l_0_4, l_0_7, l_0_9, l_0_10
  local l_3_2 = {}
  if l_3_1 == l_0_0.NIL then
    return l_0_0.INVALID_ARGUMENT
  end
  if l_3_1 == "start" then
    local l_3_3 = l_0_4 .. "." .. l_0_7.reboot
    l_3_2[l_3_3] = l_0_9
    l_3_3 = l_0_4
    l_3_3 = l_3_3 .. "." .. l_0_7.rebootTime
    l_3_2[l_3_3] = REBOOT_TIME
    l_3_3 = db
    l_3_3 = l_3_3.update
    l_3_3 = l_3_3(l_0_4, l_3_2, l_0_7.keyValue)
    status = l_3_3
  else
    do
      do
        local l_3_4, l_3_5 = (db.setAttribute)(l_0_4, l_0_7.key, l_0_7.keyValue, l_0_7.reboot, l_0_10)
        status = l_3_4
        if status == l_0_0.NIL then
          return l_0_0.FAILURE, l_3_0
        end
        return l_0_0.SUCCESS, l_3_0
      end
    end
  end
end

rebootSet = l_0_12
l_0_12 = function()
  -- function num : 0_3 , upvalues : l_0_0
  return l_0_0.NOT_SUPPORTED
end

factoryResetGet = l_0_12
l_0_12 = function(l_5_0)
  -- function num : 0_4 , upvalues : l_0_0
  return l_0_0.NOT_SUPPORTED, l_5_0
end

factoryResetGetNext = l_0_12
l_0_12 = function(l_6_0, l_6_1)
  -- function num : 0_5 , upvalues : l_0_0
  local l_6_3 = nil
  if l_6_1 == l_0_0.NIL then
    return l_0_0.INVALID_ARGUMENT
  end
  if l_6_1 == "start" then
    local l_6_2 = l_0_0.FAILURE
    if l_6_3 ~= l_0_0.NIL then
      l_6_3:close()
      l_6_2 = l_0_0.SUCCESS
    else
      l_6_2 = l_0_0.FAILURE
    end
  else
    do
      do return l_0_0.NOT_SUPPORTED end
      return l_0_0.SUCCESS, l_6_0
    end
  end
end

factoryResetSet = l_0_12
l_0_12 = function()
  -- function num : 0_6 , upvalues : l_0_0
  return l_0_0.NOT_SUPPORTED
end

backupConfigGet = l_0_12
l_0_12 = function(l_8_0)
  -- function num : 0_7 , upvalues : l_0_0
  return l_0_0.NOT_SUPPORTED, l_8_0
end

backupConfigGetNext = l_0_12
l_0_12 = function(l_9_0, l_9_1)
  -- function num : 0_8 , upvalues : l_0_0, l_0_3, l_0_7, l_0_6
  if l_9_1 == l_0_0.NIL then
    return l_0_0.INVALID_ARGUMENT
  end
  if l_9_1 ~= "start" and l_9_1 ~= "stop" then
    return l_0_0.INVALID_ARGUMENT
  end
  fileName = (db.getAttribute)(l_0_3, l_0_7.key, l_0_7.keyValue, l_0_7.name)
  local l_9_2 = (db.getAttribute)(l_0_6, l_0_7.key, l_0_7.keyValue, l_0_7.modelId)
  if l_9_0 == "pc" then
    local l_9_3 = UNIT_INFO
    local l_9_4 = string.find
    l_9_4 = l_9_4(l_9_3 or "", "-")
    if l_9_4 ~= nil and l_9_3 or "" ~= nil then
      l_9_3 = (string.sub)(l_9_3, 0, l_9_4 - 1)
    end
    do
      -- l_9_9 = nil
      if not l_9_3 then
        l_9_7, l_9_8, l_9_9, l_9_10, l_9_11, l_9_12, l_9_13, l_9_14 =  (db.getAttribute)("system", "_ROWID_", "1", "name")
      end
      if l_9_2 == "DWC-1000" then
        (util.appendDebugOut)("Exec = " .. (os.execute)("cd /tmp && mkdir backup && cp /flash/tmp/teamf1.cfg.ascii /flash/tmp/startup-config backup/"))
        -- DECOMPILER ERROR at PC83: Confused about usage of register: R6 in 'UnsetPending'

        ;
        (util.appendDebugOut)("Exec = " .. (os.execute)("cd /tmp && tar -cf" .. " " .. l_9_9 .. ".tgz" .. " " .. "backup"))
        -- DECOMPILER ERROR at PC94: Confused about usage of register: R6 in 'UnsetPending'

        -- DECOMPILER ERROR at PC97: Confused about usage of register: R6 in 'UnsetPending'

        ;
        (web.download)("/tmp/" .. l_9_9 .. ".tgz", l_9_9 .. ".tgz")
        ;
        (util.appendDebugOut)("Exec = " .. (os.execute)("rm -rf /tmp/backup  /tmp/DWC.tgz "))
      else
        local l_9_15 = nil
        if (db.getAttribute)("ConfigSupport", "_ROWID_", "1", "EncryptEnable") ~= nil and (db.getAttribute)("ConfigSupport", "_ROWID_", "1", "EncryptEnable") == "1" then
          local l_9_16, l_9_17 = nil
          local l_9_18 = nil
          -- DECOMPILER ERROR at PC131: Overwrote pending register: R8 in 'AssignReg'

          -- DECOMPILER ERROR at PC135: Overwrote pending register: R9 in 'AssignReg'

          ;
          ((io.open)("/pfrm2.0/pkgMgmt/packageKey", "r")):close()
          ;
          (util.appendDebugOut)("Exec = " .. (os.execute)("/pfrm2.0/bin/usrKlite openssl enc -aes-128-cbc -in " .. SETTINGS_FILE .. " -out " .. SETTINGS_FILE .. ".enc -K " .. nil .. " -iv " .. nil .. " -nosalt"))
          ;
          (web.download)(SETTINGS_FILE .. ".enc", l_9_17 .. ".cfg.enc")
          ;
          (util.appendDebugOut)("Exec = " .. (os.execute)("/bin/rm " .. SETTINGS_FILE .. ".enc"))
        else
          do
            do
              do
                local l_9_19 = nil
                -- DECOMPILER ERROR at PC181: Confused about usage of register: R6 in 'UnsetPending'

                ;
                (web.download)(SETTINGS_FILE, l_9_17 .. ".cfg")
                -- DECOMPILER ERROR at PC188: Confused about usage of register: R2 in 'UnsetPending'

                if l_9_0 == "usb1" then
                  if l_9_2 == "DWC-1000" then
                    (adaptos.execute)("cd /tmp && mkdir backup && cp /tmp/teamf1.cfg.ascii /mnt/fastpath/startup-config backup/")
                    ;
                    (adaptos.execute)("cd /tmp  && tar -cf" .. " " .. fileName .. ".tgz" .. " " .. "backup")
                    ;
                    (adaptos.execute)("cd /tmp && /bin/cp " .. fileName .. ".tgz" .. " " .. "/usb1")
                    usbStatusCmd = (db.getAttribute)("environment", "name", "USB_STATUS_CHECK_PROGRAM", "value")
                    ;
                    (adaptos.execute)(usbStatusCmd .. " " .. 1)
                    ;
                    (adaptos.execute)("rm -rf /tmp/backup /tmp/DWC.tgz")
                  else
                    ;
                    (adaptos.execute)("/bin/cp " .. SETTINGS_FILE .. " /usb1" .. fileName .. ".cfg")
                    usbStatusCmd = (db.getAttribute)("environment", "name", "USB_STATUS_CHECK_PROGRAM", "value")
                    ;
                    (adaptos.execute)(usbStatusCmd .. " " .. 1)
                  end
                else
                  -- DECOMPILER ERROR at PC260: Confused about usage of register: R2 in 'UnsetPending'

                  if l_9_0 == "usb2" then
                    if l_9_2 == "DWC-1000" then
                      (adaptos.execute)("cd /tmp && mkdir backup && cp /tmp/teamf1.cfg.ascii /mnt/fastpath/startup-config backup/")
                      ;
                      (adaptos.execute)("cd /tmp  && tar -cf" .. " " .. fileName .. ".tgz" .. " " .. "backup")
                      ;
                      (adaptos.execute)("cd /tmp && /bin/cp " .. fileName .. ".tgz" .. " " .. "/usb2")
                      usbStatusCmd = (db.getAttribute)("environment", "name", "USB_STATUS_CHECK_PROGRAM", "value")
                      ;
                      (adaptos.execute)(usbStatusCmd .. " " .. 2)
                      ;
                      (adaptos.execute)("rm -rf /tmp/backup /tmp/DWC.tgz")
                    else
                      ;
                      (adaptos.execute)("/bin/cp " .. SETTINGS_FILE .. " /usb2" .. fileName .. ".cfg")
                      usbStatusCmd = (db.getAttribute)("environment", "name", "USB_STATUS_CHECK_PROGRAM", "value")
                      ;
                      (adaptos.execute)(usbStatusCmd .. " " .. 2)
                    end
                  else
                    return l_0_0.NOT_SUPPORTED
                  end
                end
                do return l_0_0.SUCCESS, l_9_0 end
                -- DECOMPILER ERROR at PC337: freeLocal<0 in 'ReleaseLocals'

              end
            end
          end
        end
      end
    end
  end
end

backupConfigSet = l_0_12
l_0_12 = function()
  -- function num : 0_9 , upvalues : l_0_0
  return l_0_0.NOT_SUPPORTED
end

restoreConfigGet = l_0_12
l_0_12 = function(l_11_0)
  -- function num : 0_10 , upvalues : l_0_0
  return l_0_0.NOT_SUPPORTED, l_11_0
end

restoreConfigGetNext = l_0_12
l_0_12 = function(l_12_0)
  -- function num : 0_11 , upvalues : l_0_0, l_0_2
  local l_12_1 = l_12_0["backupRestore.restoreStatus"]
  local l_12_2 = l_12_0["backupRestore.filename"]
  local l_12_3, l_12_4, l_12_5 = nil, nil, nil
  local l_12_6 = ""
  if l_12_1 == "pc" then
    l_12_3 = (l_12_0["file.restore"]).filesize
    l_12_4 = (l_12_0["file.restore"]).filename
    l_12_5 = (l_12_0["file.restore"]).file
    if (string.sub)((l_12_0["file.restore"]).filename, -3, -1) == "enc" then
      l_12_6 = "1"
    end
  end
  local l_12_7, l_12_18, l_12_31, l_12_44, l_12_46 = nil
  if l_12_1 == l_0_0.NIL then
    return l_0_0.INVALID_ARGUMENT
  end
  if l_12_1 == "pc" then
    local l_12_8 = "out.cfg"
    local l_12_9 = nil
    if l_12_46 == "1" then
      local l_12_10, l_12_11 = ((cgilua.cookies).get)("TeamF1Login"), nil
      local l_12_12 = nil
      l_12_11 = ((io.open)("/pfrm2.0/pkgMgmt/packageKey", "r")):read("*l")
      l_12_12 = ((io.open)("/pfrm2.0/pkgMgmt/packageKey", "r")):read("*l")
      ;
      ((io.open)("/pfrm2.0/pkgMgmt/packageKey", "r")):close()
      ;
      (util.appendDebugOut)("Exec = " .. (os.execute)("/pfrm2.0/bin/usrKlite openssl enc -d -aes-128-cbc -in /tmp/" .. l_12_9 .. " -out /tmp/" .. l_12_8 .. " -K " .. l_12_11 .. " -iv " .. l_12_12 .. " -nosalt"))
      l_12_9 = l_12_8
    end
    do
      local l_12_13 = nil
      local l_12_14 = (db.getAttribute)("unitInfo", "_ROWID_", "1", "modelId")
      local l_12_15 = nil
      l_12_15:close()
      if (string.sub)(((io.popen)("cat \'" .. "/tmp/" .. l_12_9 .. "\' | grep -i \'firmwareFile\' | cut -d\'\"\' -f4 | cut -d\'_\' -f1")):read("*a"), 1, -2) ~= l_12_14 then
        (util.appendDebugOut)("Exec = " .. (os.execute)("/bin/rm -rf" .. " " .. "/tmp/" .. l_12_9 .. " ; /bin/rm -rf " .. "/tmp/" .. l_12_13))
        return l_0_2.INVALID_FILE
      else
        if (config.verifyChecksum)("/tmp/" .. l_12_9) == "ok" then
          local l_12_16 = nil
          ;
          (util.appendDebugOut)("Exec = " .. (os.execute)("cp -f" .. " " .. "/tmp/" .. l_12_9 .. " " .. (db.getAttribute)("environment", "name", "FLASH_CFG_PARTITION", "value")))
        else
          do
            do
              local l_12_17 = nil
              ;
              (util.appendDebugOut)("Exec = " .. (os.execute)("/bin/rm -rf" .. " " .. "/tmp/" .. l_12_9 .. " ; /bin/rm -rf " .. "/tmp/" .. l_12_13))
              do return l_0_2.CONFIG_CHECKSUM_FAILED end
              if l_12_1 == "usb1" then
                local l_12_19 = nil
                local l_12_20 = ""
                local l_12_21 = "out.cfg"
                if (string.sub)(l_12_7, -3, -1) == "enc" then
                  l_12_20 = "1"
                end
                if l_12_20 == "1" then
                  local l_12_22, l_12_23 = nil
                  local l_12_24 = nil
                  l_12_23 = ((io.open)("/pfrm2.0/pkgMgmt/packageKey", "r")):read("*l")
                  l_12_24 = ((io.open)("/pfrm2.0/pkgMgmt/packageKey", "r")):read("*l")
                  ;
                  ((io.open)("/pfrm2.0/pkgMgmt/packageKey", "r")):close()
                  ;
                  (util.appendDebugOut)("Exec = " .. (os.execute)("/pfrm2.0/bin/usrKlite openssl enc -d -aes-128-cbc -in /usb1/" .. l_12_22 .. " -out /tmp/" .. l_12_21 .. " -K " .. l_12_23 .. " -iv " .. l_12_24 .. " -nosalt"))
                  l_12_22 = l_12_21
                else
                  do
                    do
                      local l_12_25 = nil
                      ;
                      (util.appendDebugOut)("Exec = " .. (os.execute)("/bin/cp -f /usb1/" .. l_12_25 .. " /tmp/"))
                      local l_12_26 = nil
                      local l_12_27 = (db.getAttribute)("unitInfo", "_ROWID_", "1", "modelId")
                      local l_12_28 = nil
                      l_12_28:close()
                      if (string.sub)(((io.popen)("cat \'" .. "/tmp/" .. l_12_26 .. "\' | grep -i \'firmwareFile\' | cut -d\'\"\' -f4 | cut -d\'_\' -f1")):read("*a"), 1, -2) ~= l_12_27 then
                        (util.appendDebugOut)("Exec = " .. (os.execute)("/bin/rm -rf" .. " " .. "/tmp/" .. l_12_26))
                        return l_0_2.INVALID_FILE
                      else
                        if (config.verifyChecksum)("/tmp/" .. l_12_26) == "ok" then
                          local l_12_29 = nil
                          ;
                          (util.appendDebugOut)("Exec = " .. (os.execute)("cp -f" .. " " .. "/tmp/" .. l_12_26 .. " " .. (db.getAttribute)("environment", "name", "FLASH_CFG_PARTITION", "value")))
                        else
                          do
                            do
                              local l_12_30 = nil
                              ;
                              (util.appendDebugOut)("Exec = " .. (os.execute)("/bin/rm -rf" .. " " .. "/tmp/" .. l_12_26))
                              do return l_0_2.CONFIG_CHECKSUM_FAILED end
                              if l_12_1 == "usb2" then
                                local l_12_32 = nil
                                local l_12_33 = ""
                                local l_12_34 = "out.cfg"
                                if (string.sub)(l_12_7, -3, -1) == "enc" then
                                  l_12_33 = "1"
                                end
                                if l_12_33 == "1" then
                                  local l_12_35, l_12_36 = nil
                                  local l_12_37 = nil
                                  l_12_36 = ((io.open)("/pfrm2.0/pkgMgmt/packageKey", "r")):read("*l")
                                  l_12_37 = ((io.open)("/pfrm2.0/pkgMgmt/packageKey", "r")):read("*l")
                                  ;
                                  ((io.open)("/pfrm2.0/pkgMgmt/packageKey", "r")):close()
                                  ;
                                  (util.appendDebugOut)("Exec = " .. (os.execute)("/pfrm2.0/bin/usrKlite openssl enc -d -aes-128-cbc -in /usb2/" .. l_12_35 .. " -out /tmp/" .. l_12_34 .. " -K " .. l_12_36 .. " -iv " .. l_12_37 .. " -nosalt"))
                                  l_12_35 = l_12_34
                                else
                                  do
                                    do
                                      local l_12_38 = nil
                                      ;
                                      (util.appendDebugOut)("Exec = " .. (os.execute)("/bin/cp -f /usb2/" .. l_12_38 .. " /tmp/"))
                                      local l_12_39 = nil
                                      local l_12_40 = (db.getAttribute)("unitInfo", "_ROWID_", "1", "modelId")
                                      local l_12_41 = nil
                                      l_12_41:close()
                                      if (string.sub)(((io.popen)("cat \'" .. "/tmp/" .. l_12_39 .. "\' | grep -i \'firmwareFile\' | cut -d\'\"\' -f4 | cut -d\'_\' -f1")):read("*a"), 1, -2) ~= l_12_40 then
                                        (util.appendDebugOut)("Exec = " .. (os.execute)("/bin/rm -rf" .. " " .. "/tmp/" .. l_12_39))
                                        return l_0_2.INVALID_FILE
                                      else
                                        if (config.verifyChecksum)("/tmp/" .. l_12_39) == "ok" then
                                          local l_12_42 = nil
                                          ;
                                          (util.appendDebugOut)("Exec = " .. (os.execute)("cp -f" .. " " .. "/tmp/" .. l_12_39 .. " " .. (db.getAttribute)("environment", "name", "FLASH_CFG_PARTITION", "value")))
                                        else
                                          do
                                            do
                                              local l_12_43 = nil
                                              ;
                                              (util.appendDebugOut)("Exec = " .. (os.execute)("/bin/rm -rf" .. " " .. "/tmp/" .. l_12_39))
                                              do return l_0_2.CONFIG_CHECKSUM_FAILED end
                                              do
                                                local l_12_45, l_12_47 = l_0_0.FAILURE
                                                do return l_12_47 end
                                                return l_0_0.SUCCESS, l_12_7
                                              end
                                            end
                                          end
                                        end
                                      end
                                    end
                                  end
                                end
                              end
                            end
                          end
                        end
                      end
                    end
                  end
                end
              end
            end
          end
        end
      end
    end
  end
end

restoreConfigSet = l_0_12
l_0_12 = function()
  -- function num : 0_12 , upvalues : l_0_0
  return l_0_0.NOT_SUPPORTED
end

restoreConfigFileGet = l_0_12
l_0_12 = function(l_14_0)
  -- function num : 0_13 , upvalues : l_0_0
  return l_0_0.NOT_SUPPORTED, l_14_0
end

restoreConfigFileGetNext = l_0_12
l_0_12 = function(l_15_0, l_15_1)
  -- function num : 0_14 , upvalues : l_0_0
  return l_0_0.NOT_SUPPORTED, l_15_0
end

restoreConfigFileSet = l_0_12
l_0_12 = adaptos
l_0_12.execute = function(l_16_0)
  -- function num : 0_15
  status = (os.execute)(l_16_0)
  return status
end

l_0_12 = function()
  -- function num : 0_16 , upvalues : l_0_5, l_0_7, l_0_11, l_0_0
  local l_17_0 = (db.getAttribute)(l_0_5, l_0_7.name, l_0_11, l_0_7.bootupTime)
  if l_17_0 == l_0_0.NIL then
    return l_0_0.FAILURE
  end
  return l_0_0.SUCCESS, l_17_0
end

bootupTimeGet = l_0_12
l_0_12 = function(l_18_0)
  -- function num : 0_17 , upvalues : l_0_2, l_0_0
  local l_18_1 = (io.open)(l_18_0, "r")
  local l_18_2 = l_18_1:seek()
  local l_18_3 = l_18_1:seek("end")
  l_18_1:seek("set", l_18_2)
  if l_18_3 > 2097152 then
    return l_0_2.FILE_SIZE_MORE_THAN_2MB, l_18_3
  else
    return l_0_0.SUCCESS, l_18_3
  end
end

fileSizeGet = l_0_12

