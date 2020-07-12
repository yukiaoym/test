import requests
import bs4
import re
import glob

def main():
    fname = glob.glob('kamiyawar*.txt')
    with open(fname[0], 'r', encoding="utf-8") as in_f:
        l = in_f.readlines()
        n = 2
        m = n + 1
        url = l[m]
        with open('./out/{}'.format(fname[0]), 'w', encoding="utf-8") as out_f:
            print(l[0], l[1], file=out_f)
            while n < len(l):
                title = l[n]
                url = l[m]
                print(title, url, file=out_f)
                usr, que, ans = get_qa(url)
                print(usr + '\n' + que + '\n' + '【kam********さん】' + '\n' + ans + '\n', file=out_f)
                n = n + 2     
            

    url = input("URL ")
    
    # Delete html tag
    def del_html(contents):
        contents = str(contents)
        tags = re.compile(r"<[^>]*?>")
        text_contents = tags.sub("", contents)
        return text_contents

    # Get Q&A
    def get_qa(url):

        # Get answer
        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        kamiyawar_id = '<p class="usrNm"><a href="https://chiebukuro.yahoo.co.jp/my/101713799">kam********</a>さん</p>'
        elems_ans = soup.select('p')

        def get_index():
            for i, p in enumerate(elems_ans):
                p = str(p)
                if kamiyawar_id in p:
                    return(i)
        
        index = get_index() + 2
        ans = elems_ans[index]
        ans = del_html(ans)


        # Get question
        elems_usr = soup.select('p.usrNm')

        usr = elems_usr[0]
        usr = del_html(usr)
        usr = "【" + usr + "】"

        elems_ptsQes = soup.select('.ptsQes')
        elems_que = elems_ptsQes[0].select('p')

        que0 = elems_que[0]
        que0 = del_html(que0)
        que0 = que0.replace('\t', '')

        que1 = elems_que[1]
        que1 = del_html(que1)
        que1 = que1.replace('\t', '')

        que = que0 + que1

        return usr, que, ans

    # Print Q&A
    usr, que, ans = get_qa(url)
    print(usr + '\n' + que + '\n' + '【kam********さん】' + '\n' + ans)


if __name__ == '__main__':
    main()