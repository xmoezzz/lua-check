function aaa(m, n)
    local a = 1
    local b = 1
    function bbb(k, j)
        function ccc()
            a = b
            return a
        end
    end
    return bbb
end

function test()
    aaa(1,2)
end
