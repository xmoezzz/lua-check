LuaQ                      A@  @ $     $@  À  $    $À  @ $           require    teamf1lualib/fwView    customServicesCfgInit    customServicesCfgSave    customServicesCfgDel    customServicesCfgInputVal    customServicesCfgGet           *     :   F @    @  À  À   AÂ  A @  @  ÀA	À   BÁ@ A @  @  @  @  ÁÀ @      @  Æ@C À @  CWÀCÀ@  CW DÀ @  C@D @  Å@  ÆÀÄÀ À @  Å@  ÆÀÄÀ @  @EÅ@              ð?
   configRow     db    getDefaults 	   Services    Services.DestinationPortEnd    0    getRow    _ROWID_    printCLIError    Row does not exist!
 
   operation        @   Services.Protocol    6    17    256    Services.DestinationPortStart1    Services.DestinationPortStart    Services.DestinationPortStart2    Services._ROWID_                     -   L     	B   A   @  Á@  Á    A W@A@A WA A ÀA AB 	 @ B 	 	ÀÂ	ÀBA  C  	ÃÁC ÀB	ÀB	Ã ÁD@   ÁA Á  @  À ÁD@  ÁC Á Á  @   À  Á FA Á AFA Á À  Û@   À    @        OK        DBTable 	   Services    Services.Protocol    6    17    256    Services.DestinationPortStart    Services.DestinationPortStart1    Services.DestinationPortStart2     1    Services.DestinationPortEnd    0    Services._ROWID_    Services.OID    Services.IsDefault    fwView    serviceConfig    -1    add    edit    db    save    getAttribute    stringsMap 	   stringId 	   LANGUAGE                     O   s     ]   A   @  Á@  @ A GÁ  E FÁÁ Á   \ GA EA @Â@E Á \A @ ^EA FÃ@Ã E  \A B  ^ E FÁÃ Á   A \ ADÁ Â @ Å ÆAÄB AÂ Á UÂÜA  @ Ú  À A ÁÂ UÂB    
  EB FBÆ	BE FÂÆ \Â   @  Ç  E FBÇ\B E FÂÃ ÁÂ   E \À @ ^  !      ERROR           ð?   DBTable 	   Services 
   configRow    db    getRow    _ROWID_     printCLIError    Row doesnt exist!
    Services.IsDefault    1 .   Cannot delete a row with service as default!
    getAttribute    ServiceName    existsRowWhere    FirewallRules    ServiceName = '    '    FirewallRules6    Cannot delete service:      as it is in use!
    rowid    Services._ROWID_    fwView    deleteServices    OK    save    stringsMap 	   stringId 	   LANGUAGE                     u   
    	  F @ @À @E  FÀÀ   Á@ A AÁ \ B W@  @ Á @        À@Á  A FA Á F C @Ã  E@  \@ B   ^  F B WÀÃ  F B  Ä  E@ @ \@ B   ^  FD W Ä  FD ÀÃ  E@ À \@ B   ^  F E W Ä  F E ÀÃ  E@ @ \@ B   ^  F E Å À<FD W@Ã  FD ÀÅ  F F  Ä @E@ @ \@ B   ^  
FD @Ã F F W Ä ÀE  F \ XÀÆ  E  F \ @ E@ @ \@ B   ^   FD ÀÅ @F F W Ä E  F \ XÇ  E  F \ @ E@   \@ B   ^  FD @Ã ÀF F  Ä  E@ @ \@ B   ^  FD @Ã @F F W Ä E  F \ XÀÆ  E  F \ @  E@  \@ B   ^  FD WÀÈ @FD W É  FD @É @FI W Ä @FÀI W Ä  FÀI ÀÃ  E@  
 \@ B   ^  FD W@Ã  FD ÀÅ À 	 DF F 	@ 	 DFI 	@FD WÀÈ @FD W É  FD @É F@J W Ä ÀFÀI W Ä  E ÀI \  Æ@J    E@ 
 \@ B   ^  FD W@Ã  FD ÀÅ  F F  Ä @E@ À
 \@ B   ^  
FD @Ã F F W Ä ÀE  F \ XÀÆ  E  F \ @ E@   \@ B   ^   FD ÀÅ @F F W Ä E  F \ XÇ  E  F \ @ E@ @ \@ B   ^  FD WÀÈ @FD W É  FD @É @FI W Ä  FÀI  Ä  E@  
 \@ B   ^  FÀI W Ä  FÀI Å  E@  \@ B   ^  	 ÄF E  Ì ÀFD WÀÈ @FD W É  FD @É FÀK W Ä  FÀK ÀÃ  E@ @ \@ B   ^  FD @Ã  E@  \@ B   ^  EÀ F Í ÀK Á@ \ À   Å   Ü YÀÆ Å   Ü À ÅA  ÜA Â  Þ ¡  û	 Ä	 ÄF @ @À E  FÀÀ   Á@ A AÁ \ B W@  @ Á@ @      E  FÀÀ  Á@ A AÁ \Z@    AÀ W Ï ÀD ÀE @ Á@ @            >   
   operation    edit    db    getAttribute 	   Services    _ROWID_    Services._ROWID_    ServiceName    Services.ServiceName    printCLIError ;   You cannot edit the service name of already existing row!
 	   Protocol    Services.IsDefault    1 ,   Cannot edit a row with service as default!
         Enter unique service name!
    Services.Protocol    Enter valid protocol name!
    Services.PortType    Enter valid port type name
    0    58    Services.DestinationPortStart2    Enter valid ICMP type
 	   tonumber               D@$   Enter valid ICMP type between 0-40
       ð?     ào@'   Enter valid ICMPv6 type between 1-255
    Enter valid ICMP type!
 %   Enter valid ICMP type between 0-40!
    6    17    256    Services.DestinationPortStart1    Services.DestinationPortEnd    Enter valid Port Range
    Services.DestinationPortStart Z   please enter valid values destinationport end can not be less than destination port start    Enter valid ICMP Port
 $   Enter valid ICMP Port between 0-40
 %   Enter valid ICMP Port between 1-255
    Enter finish_port!
    Services.MultiPort    2    Enter valid Multiple Ports
 2   ICMP Protocol can't be configured with multiport
    util    split    ,    pairs     àÿï@-   Enter valid Multiple Ports between 1-65535 
 8   you cannot edit the service name of already existed Row    networkInfo    netWorkMode    3 =   Change IpMode for Adding Custom Service for ICMPv6 Protocol
                       <     ¬      @@ A   J     ÁÀ   AA A  @  @%ÌÀÁFÂ  W Â@$BÂÀ@# ÂBÀ  FCÃZC    A B  ÂBÀ Ã FÄZC    A B BÄD ÂBÀ Ã A B  BÄ@E ÂBÀ Ã A B 	BÄÀE ÂBÀ Ã A B  BÄ@F ÂBÀ Ã A B BÄ@F ÂBÀ Ã A B  BÄ G@ ÂBÀ Ã AC B ÇÀ@ BÄWD BÄ GÀ ÂBÀ Ã AÃ B  ÂBÀ  FCÈB BÄW@E@BÄWÀE BÄ@F@ ÂBÀ Ã A B BÈÁÂ ÉÅ ÆÂÂ  A C    ÜB Ç@I ÂBÀ Ã A	 B  ÂBÀ  FÃÉZC    A B !  ÀÙ J@ A
 A  *      db 	   getTable 	   Services    0    printLabel "   List of Available Custom Services    pairs       ð?    Services.IsDefault    resTab    insertField    ROW ID    Services._ROWID_        Name    Services.ServiceName    Services.Protocol    1    Protocol Type    ICMP    6    TCP    17    UDP    256    BOTH    Type    58    ICMPv6    Services.PortType    ICMP/ICMPv6 "   ICMP Type / Port Range / Multiple    Services.DestinationPortStart    RANGE    -    Services.DestinationPortEnd    2 	   MULITPLE    Services.MultiPort    print                                     