LuaQ                      A@  @ À    @   $    $@  À $    $À  @   
      require    teamf1lualib/fwView    rowid    1    totalLimit        trafficMeterCfgSave    trafficMeterCfgInit    trafficMeterCfgInputVal    trafficMeterSetupGet                "   A@  G   A@  G  A@  GÀ  A@ G  E FÀÁ    Å  A \À   G   E   Â  EÀ F Ã \@ EÀ F@Ã  ÁÀ   E \GÀ  E   À  ^      
   errorFlag        statusCode    statusMessage    DBTable    FwTrafficMeter    fwView    trafficMeterConfig    rowid    edit    OK    db    save    getAttribute    stringsMap 	   stringId 	   LANGUAGE                         ,     +   E@  FÀ À  Á  A \ G   E   Á  J   G   @E   FÀÁ @Á @E   F Â W@Â @E   FÂ @Á E     @C\   Å   ÆÃ L GÀ  E   F@Ã GÀ EÀ    ^      
   configRow    db    getRow    FwTrafficMeter    _ROWID_    1  "   FwTrafficMeter.TrafficMeterStatus     FwTrafficMeter.TrafficLimitType    0 #   FwTrafficMeter.IncreaseLimitStatus    totalLimit 	   tonumber #   FwTrafficMeter.TrafficMonthlyLimit    FwTrafficMeter.IncreaseLimitBy    rowid                     .   0        B  ^                            2   r     	  J   @  @ÁÀ   EA        AÀ À Á  @  *@ Á @    ÀB CÀ À Á@ @ @'   ÀBC@&À ÁÀ @     D C  @      DC À @ @    D E@ @ @ À Á A AÁ Õ@@ À Á    AFAÁ Õ@@    FCÀ ÁÀ @     GWAÀ Á@   GAÁ Õ@@  À Á @ À ÁÀ  AÁ Õ@@ @ Á@ @    HCÀ À ÁÀ @    H C À Á 	 @    @IWAÀ   IWAÀ   ÀIWAÀÀ Á 
   AIAA
   IÁ
   ÂIÕ @    ÀJCÀ À Á  @    ÀJ C À Á@ @ @ Á @    ÀK C @   @    À ÁÀ  A Õ@@    @MCÀ À Á @    @MC À ÁÀ @ @  @Á@  EA      WA@ Á @ À  OÀ  A E FÏZA    AÁ @ À  OÀ   E FAÐZA    AÁ @ À  OÀ   E FÁÐZA    AÁ @ À  OÀ   E FAÑZA    AÁ @ À  OÀ   E FÁÑZA    AÁ @ À  OÀ   E FAÒZA    AÁ @ À ÀAÀ   @  K      tmRow    db    getRow    FwTrafficMeter    _ROWID_    rowid     print *   Traffic Meter configurations unavailable
    printLabel    Enable Traffic Meter "   FwTrafficMeter.TrafficMeterStatus    0    Traffic Meter is Disabled
    1    Traffic Meter is Enabled
     FwTrafficMeter.TrafficLimitType 
   limitType 	   No Limit    Download only    2    Both Directions    Limit Type     
    Monthly Limit in (MB):  #   FwTrafficMeter.TrafficMonthlyLimit #   FwTrafficMeter.IncreaseLimitStatus %   Increase this month limit: Enabled 
    FwTrafficMeter.IncreaseLimitBy    Increase limit by in (MB):  &   Increase this month limit: Disabled 
    This month limit:     totalLimit    Traffic Counter
    FwTrafficMeter.RestartCounter     Traffic Counter: Specific Time
 "   Traffic Counter: Restart Counter
    FwTrafficMeter.TimeHH    FwTrafficMeter.TimeMM    FwTrafficMeter.DayOfMonth $   Restart Time (HH/MM-Day of Month):     /    -    FwTrafficMeter.SendEmailReport (   Send e-mail before restarting: Enabled
 )   Send e-mail before restarting: Disabled
    When Limit is reached
    FwTrafficMeter.BlockTraffic    blockTraffic    Block All Traffic    Block All Traffic Except Email    Traffic Block Status:      
    FwTrafficMeter.SendEmailAlert    Send e-mail alert: Enabled
    Send e-mail alert: Disabled
    tsRow    TrafficStatistics    Internet Traffic Statistics
    resTab    insertField    Start Date / Time    TrafficStatistics.StartTime        Outgoing Traffic Volume "   TrafficStatistics.OutgoingTrafVol    Incoming Traffic Volume "   TrafficStatistics.IncomingTrafVol    Average per day    TrafficStatistics.AvgPerDay    % of Standard Limit     TrafficStatistics.StandardLimit    % of this Month's Limit !   TrafficStatistics.ThisMonthLimit                                     