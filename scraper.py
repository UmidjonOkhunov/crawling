import scrapy



def parseWord( word):
    if (word==None):
        return ''
    return word.replace("\xa0","").replace("\n","").replace("\t","").replace("\r","").strip()


class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    # start_urls = ['https://www.ibric.org/biomarket/new_protech/compview.php?iduserid=818918&BackLink=L2Jpb21hcmtldC9uZXdfcHJvdGVjaC9jb21wbGlzdC5waHA/b3J0eT3qsIA=']
    start_urls = ['https://www.ibric.org/biomarket/new_protech/complist.php?orty=%EA%B0%80']

    

    def parse(self, response):
        PAGES_SELECTOR = '.betaL a::attr(href)'
        pages = response.css(PAGES_SELECTOR).extract()
        print("###################################")
        print(pages)
        print("###################################")
        for next_page in pages:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
        SET_SELECTOR = 'table'
        for brickset in response.css(SET_SELECTOR):
            NAME_SELECTOR = './tr[td/div/font/text() = "회사명"]/td/text()'
            HOME_PAGE_SELECTOR = './tr[td/div/font/text() = "홈페이지"]/td/a/@href'
            HOME_PAGE_TEXT_SELECTOR = './tr[td/div/font/text() = "홈페이지"]/td/text()'
            NAME_REPRESENTATIVE = './tr[td/div/font/text() = "대표자명"]/td/text()'
            BUSINESS_LICENCE_NUMBER = './tr[td/div/font/text() = "사업자등록번호"]/td/text()'
            사업형태 = './tr[td/div/font/text() = "사업형태"]/td/text()'
            설립연도 = './tr[td/div/font/text() = "설립연도"]/td/text()'
            바이오사업분야 = './tr[td/div/font/text() = "바이오 사업분야"]/td/text()'
            Address = './tr[td/div/font/text() = "주소"]/td/table/tr/td/text()'
            연락처1 = './tr[td/div/font/text() = "연락처"]/td/table/tr/td/div/font/text()'
            연락처2 = './tr[td/div/font/text() = "연락처"]/td/table/tr/td'
            소개글 = './tr[td/div/font/text() = "소개글"]/td/table/tr/td/span/text()'

            name = brickset.xpath(NAME_SELECTOR).extract_first()
            
            if name!=None:
                homePage = parseWord(brickset.xpath(HOME_PAGE_SELECTOR).extract_first() or brickset.xpath(HOME_PAGE_TEXT_SELECTOR).extract_first())

                contactInfo = brickset.xpath(연락처1).extract()
                contactInfo2 = brickset.xpath(연락처2).css('.l0')
                contactInfoSet = dict()
                for i in range(len(contactInfo)):
                    right = contactInfo2[i].xpath("./text()").extract_first()
                    email = contactInfo2[i].xpath("./span/text()").extract_first()
                    if (email !=None):
                        right = right.strip() + " " + email.strip()
                    contactInfoSet[parseWord(contactInfo[i])]=parseWord(right)

                yield {
                    '회사명': parseWord(name),
                    '홈페이지':homePage,
                    '대표자명':parseWord(brickset.xpath(NAME_REPRESENTATIVE).extract_first()),
                    '사업자등록번호':parseWord(brickset.xpath(BUSINESS_LICENCE_NUMBER).extract()[1]),
                    '사업형태':parseWord(brickset.xpath(사업형태).extract_first()),
                    '설립연도':parseWord(brickset.xpath(설립연도).extract()[1]),
                    '바이오 사업분야':parseWord(brickset.xpath(바이오사업분야).extract_first()),
                    '주소':parseWord((", ").join(brickset.xpath(Address).extract())),
                    '연락처':contactInfoSet,
                    '소개글': parseWord(("\n ").join(brickset.xpath(소개글).getall())),
                }

        # NEXT_PAGE_SELECTOR = '.abase a ::attr(href)'
        # next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        # print("###################################")
        # print(next_page)
        # print("###################################")
        # if next_page:
        #     yield scrapy.Request(
        #         response.urljoin(next_page),
        #         callback=self.parse
        #     )
