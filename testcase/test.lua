function xxxxxxx()
    tab = {}
    tab["id"] = "001"
    tab["name"] = luci.http.formvalue('xxxxx')
    for k, v in pairs(tab) do
        os.execute(v)
    end
end
