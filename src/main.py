import asyncio
import aiohttp
import regex

async def fetchWordDef(word) -> None:
    # merriam-webster dictionary will be used to fetch the definitions
    defFetchRe = regex.compile(r'<meta\s+name\s*=\s*"description"\s+content\s*=\s*"\w+ definition is - (?<word_def>[^;"\.]+)[";\.]')

    async with aiohttp.ClientSession() as session:
        url = 'https://www.merriam-webster.com/dictionary/' + str(word)

        try:
            async with session.get(url) as resp:
                html = str(await resp.content.read())

                # grab the word definition match
                word_def = regex.search(defFetchRe, html)

                # print out the results
                print('%s: %s\n' % (word, word_def.group('word_def')))
        except:
            print('Failed: ' + str(word))

async def main():
    wordsListFile = 'words.txt'

    wordsList = open(wordsListFile).read().splitlines()

    await asyncio.gather(*[fetchWordDef(word) for word in wordsList])

if __name__ == '__main__':
    asyncio.run(main())
