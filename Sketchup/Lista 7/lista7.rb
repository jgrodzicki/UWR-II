def palindrome?(text)
  if text == ""
    return true
  end
  text.downcase!.gsub!(/\W/, '')
  text == text.reverse
end

print "Palindrome?:\n"
print "A man, a plan, a canal -- Panama", "\t=>\t", palindrome?("A man, a plan, a canal -- Panama"), "\n"
print "Madam, I'm Adam!", "\t=>\t", palindrome?("Madam, I'm Adam!"), "\n"
print "Abracadabra", "\t=>\t", palindrome?("Abracadabra"), "\n"
print "", "\t=>\t", palindrome?(""), "\n\n"

def count_words(text)
  if text == ""
    return {}
  end
  text.downcase!.gsub!(/\W/, ' ')
  cnt = {}
  for word in text.split(' ')
    if cnt.key?(word)
      cnt[word] += 1
    else
      cnt[word] = 1
    end
  end
  cnt
end

print "Count_words:\n"
print "A man, a plan, a canal -- Panama", "\t=>\t", count_words("A man, a plan, a canal -- Panama"), "\n"
print "Madam, I'm Adam!", "\t=>\t", count_words("Madam, I'm Adam!"), "\n"
print "Abracadabra", "\t=>\t", count_words("Abracadabra"), "\n"
print "AAa aaA aAa" , "\t=>\t", count_words("AAa aaA aAa"), "\n"
print "", "\t=>\t", count_words(""), "\n\n"


def same23?(arr)
  if arr.length != 5
    return false
  end

  cnt = {'a'=>0, 'b'=>0, 'c'=>0}
  for el in arr
    cnt[el] += 1
  end

  c = cnt.values.sort
  c[1] == 2 and c[2] == 3
end

print "Same23?:\n"
print ["a", "a", "a", "b", "b"], "\t=>\t", same23?(["a", "a", "a", "b", "b"]), "\n"
print ["a", "b", "c", "b", "c"], "\t=>\t", same23?(["a", "b", "c", "b", "c"]), "\n"
print ["a", "a", "a", "a", "a"], "\t=>\t", same23?(["a", "a", "a", "a", "a"]), "\n"

