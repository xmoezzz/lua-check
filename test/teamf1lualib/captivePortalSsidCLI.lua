LuaQ                @      A@  @ 
       	 Α  	Α  	 Β  	Β
   ΐ ΐ 	 Aΐ 	Αΐ 	 Bΐ 	Β
       	Α  	 B  	Β  	@E
     	 Α 	@F 	ΐF 	@G 	ΐG 	@H 	Θ 	 Ι 	Ι$   ΐ	 $@   
 $  @
 $ΐ  
 $  ΐ
   ,      require    teamf1lualib/captivePortal    accessType    free    0    SLA    1 
   permanent    2 
   temporary    3 	   authMode 
   localUser    radiusServer    LDAPServer    POP3 	   authType    PAP    CHAP    MSCHAP 	   MSCHAPv2    4    authServerId    localDatabaseUser 
   radiusPAP    11    radiusCHAP    12    radiusMSCHAP    13    radiusMSCHAPv2    14    LDAP    20    50    activeDirectory    30 	   NTdomain    40    captivePortalSsidCfgInit    captivePortalSsidCfgSave    captivePortalSsidCfgInputVal    captivePortalSsidShow    captivePortalShowProfile        1   5        J   @@ I @  ΐ           CaptivePortalSSID.ssid       π?                    8   X     W   A   @  Α@    Α@FA  J  AA IAA Ε ΖΑΑWΐ AA Ε ΖΒΐΐAA Ε ΖΑΑΐ@ ΑAIAB   @ΑB CΖAB ΑI@ΑB    ΑB CIAC IC I@AA Ε ΖΑΓΐ  I IIAD  Dΐ  AΒ Α  @   ΐ   AEA  EΑΑ  @ B Ϋ@   Α@   ΫA  ΑA          OK        captivePortal    getCPInterfaceRow    CaptivePortalSSID.ssid    CaptivePortalSSID.accessType    accessType 
   permanent 
   temporary    CaptivePortalSSID.authType    CaptivePortalSSID.authServerId    CaptivePortalSSID.authMode       $@   CaptivePortalSSID.profileId    CaptivePortalSSID.redirectType    SLA    NULL    1    cpInterfaceConfig    edit    db    save    getAttribute    stringsMap 	   stringId 	   LANGUAGE                     ]           E   F@ΐ @ \ ΐΐ    Α@ @      A ΐ@   Αΐ @      A Ε  Ζ@ΒWΐ  A Ε  ΖΒΐ  	A Ε  Ζ@Βΐ ΐΐB ΐ@   Α  @      A Ε  ΖΒΐ ΐΐB ΐ@   Α@ @         CΖΐB  ΐ@ Ε  Α ά@ Β   ή  A Ε  ΖΒΐ ΐ D ΐ@   Α@ @      A Ε  ΖΒΐ   D Ε ΖΐΔΐ ΐ E ΐ@   Α@ @      A Ε  ΖΕWΐ  A Ε  ΖΐΕΐ ΐΐB Wΐ@   Α  @      A Ε  ΖΒWΐ  D ΐ@  E Wΐ@   Α@ @       E Wΐ@@ D Ε ΖΐΔWΐ    Α @                  captivePortal    getCPInterfaceRow    CaptivePortalSSID.ssid     print 4   Please enter valid SSID to configure captive portal    CaptivePortalSSID.accessType "   Please enter Access Type for SSID    accessType 
   temporary 
   permanent    CaptivePortalSSID.profileId 5   Please enter temporary-user Captive Portal ProfileId 5   Please enter permanent-user Captive Portal ProfileId    getCPprofileIdRow ~   Given Captive Profile Id doesn't exists,give a valid CP-profile Id,use showCP-profiles command to get the list of CP Profiles    CaptivePortalSSID.authMode 9   Please enter Authentication Mode for authenticating user 	   authMode    radiusServer    CaptivePortalSSID.authType 3   Please enter Authentication type for Radius Server    SLA    free V   Incorrect Access Type,only permanent or temperory users can have CP Profile settings. h   Incorrect Access Type,only permanent user can have authentication mode or authentication type settings. H   Incorrect settings,authentication type is supported in Radius mode only                        Μ      ―      @@ A   J     Αΐ   Α B A B ΐA ΐ  AB B & @  ΐ#ΜΐΒΐ  WΐAΐ"FCCZC    A G FΓCZC    A G FCDZC    A G E  ΓD@   E  CE@  @E  ΓE@  
E  CF@  ΐE  ΓF@   E  CG@ A @E  G@  E  ΓG@  ΐE  CH@     FIZC    A GΓ EΓ C	 I AΑ	 
  EΓ C	 CJ A
    A
 FKZC    A GΓ
 EC FΛ ΑΓ  D     \C EC FΛ Α  D     \C EC FΛ ΑC D   \C EC FΛ Α D    \C !  @ΫB B@ Β  B  3      db 	   getTable    CaptivePortalSSID                printLabel 4   -------------CP SSID Configuration----------------
     print    There are no entries in system    pairs       π?
   networkId    CaptivePortalSSID.networkId    ssid    CaptivePortalSSID.ssid    authServer    CaptivePortalSSID.authServerId    authServerId    localDatabaseUser    Local User Database 
   radiusPAP    Radius-PAP    radiusCHAP    Radius-CHAP    radiusMSCHAP    Radius-MSCHAP    radiusMSCHAPv2    Radius-MSCHAPV2    LDAP    POP3    activeDirectory    Active Directory 	   NTdomain 
   NT-Domain 
   accessTyp    CaptivePortalSSID.accessType    accessType    free 	   Disabled    None    SLA    Enabled 
   profileId    CaptivePortalSSID.profileId    resTab    insertField    Network-Id    SSID    Captive-Portal    AuthServer                     Π   η      >      @@ A   J     Αΐ   A A Α A ΐA ΐ  ΑA A 
 ΐ  ΐΜΐΒΐ  WΐAΐΖBCΪB    Α Η ΖΒCΪB    Α Η Ε ΖBΔ  A  C     άB Ε ΖBΔ  AΓ  C     άB ‘  @χ Bΐ Β  A        db 	   getTable    CaptivePortalPageDetails                printLabel 6   -------------Captive Portal Profiles----------------
     print    There are no entries in system    pairs       π?
   profileId #   CaptivePortalPageDetails.profileId    profileName +   CaptivePortalPageDetails.configurationName    resTab    insertField    Profile-Id    Profile Name                             