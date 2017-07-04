import time
import xlsxwriter
def make_lists_of_list(li,chunk_size):
    li_of_li = []
    counter = 0
    temp_list = []
    flag = False
    for elem in li:
        temp_list.append(elem)
        counter += 1
        flag = False
        if counter >= chunk_size:
            flag = True
            li_of_li.append(temp_list)
            temp_list = []
            counter = 0
    
    if flag == False:
        li_of_li.append(temp_list)
        
    return li_of_li 


def save_links_to_text_file(urls_tup_list):
    f = open("stage2.txt","w+")
    for tup in urls_tup_list:
        f.write(tup[0]+"***"+tup[1]+"\n")
    f.close()

def put_data_to_excel(data_list):
    
    workbook = xlsxwriter.Workbook("{}.xlsx".format("Data"))
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "SKU")
    worksheet.write(0, 1, "Name")
    worksheet.write(0, 2, "Price")
    worksheet.write(0, 3, "Parent SKU")
    worksheet.write(0, 4, "Parent/Child")
    worksheet.write(0, 5, "Option1")
    worksheet.write(0, 6, "Option2")
    worksheet.write(0, 7, "Category")
    worksheet.write(0, 8, "Available")
    worksheet.write(0, 9, "Bulletpoint1")
    worksheet.write(0, 10, "Bulletpoint2")
    worksheet.write(0, 11, "Bulletpoint3")
    worksheet.write(0, 12, "Bulletpoint4")
    worksheet.write(0, 13, "Bulletpoint5")
    #new addition 
    worksheet.write(0, 14, "Variation Theme")
    worksheet.write(0,15, "Main Image URL")
    worksheet.write(0,16, "Other Image URL")
    worksheet.write(0,17, "Other Image URL")
    worksheet.write(0,18, "Other Image URL")
    worksheet.write(0,19, "Other Image URL")
    worksheet.write(0,20, "Other Image URL")
    worksheet.write(0,21, "Other Image URL")
    worksheet.write(0,22, "Other Image URL")



    row = 0
    for parent_dic in data_list:
        row += 1
        worksheet.write(row, 0, parent_dic["sku"])
        worksheet.write(row, 1, parent_dic["name"])
        worksheet.write(row, 2, parent_dic["price"])
        worksheet.write(row, 3, "")
        worksheet.write(row, 4,"parent")
        worksheet.write(row, 5, "")
        worksheet.write(row, 6, "")
        worksheet.write(row, 7, parent_dic["category"])
        worksheet.write(row, 8, parent_dic["available"])
        worksheet.write(row, 9, parent_dic["b1"])
        worksheet.write(row, 10, parent_dic["b2"])
        worksheet.write(row, 11, parent_dic["b3"])
        worksheet.write(row, 12, parent_dic["b4"])
        worksheet.write(row, 13, parent_dic["b5"])
        
        # vr_theme
        if parent_dic["vr_theme"] == 1:
            worksheet.write(row, 14, "Color")
        elif parent_dic["vr_theme"]==2:
            worksheet.write(row,14,"Color Size")
        else:
            worksheet.write(row,14,"")    
        
        worksheet.write(row, 15, parent_dic["image_url"])

        #other images 
        worksheet.write(row,16, parent_dic["i1"])
        worksheet.write(row,17, parent_dic["i2"])
        worksheet.write(row,18, parent_dic["i3"])
        worksheet.write(row,19, parent_dic["i4"])
        worksheet.write(row,20, parent_dic["i5"])
        worksheet.write(row,21, parent_dic["i6"])
        worksheet.write(row,22, parent_dic["i7"])

         

        for child_dic in parent_dic["children"]:
            row += 1
            worksheet.write(row, 0, child_dic["sku"])
            worksheet.write(row, 1, parent_dic["name"])
            worksheet.write(row, 2, parent_dic["price"])
            worksheet.write(row, 3,parent_dic["sku"])
            worksheet.write(row, 4,"child")

            temp_list = child_dic["sku"].split('-')
            
            if len(temp_list) > 2:
                worksheet.write(row, 5, temp_list[-2])
                worksheet.write(row, 6, temp_list[-1])
            else:
                worksheet.write(row, 5, temp_list[-1])
                worksheet.write(row, 6, "")

            
            worksheet.write(row, 7, parent_dic["category"])
            worksheet.write(row, 8, child_dic["available"])
            
            #bullet points 
            worksheet.write(row, 9, parent_dic["b1"])
            worksheet.write(row, 10, parent_dic["b2"])
            worksheet.write(row, 11, parent_dic["b3"])
            worksheet.write(row, 12, parent_dic["b4"])
            worksheet.write(row, 13, parent_dic["b5"])

            # vr_theme
            if parent_dic["vr_theme"] == 1:
                worksheet.write(row, 14, "Color")
            elif parent_dic["vr_theme"]==2:
                worksheet.write(row,14,"Color Size")
            else:
                worksheet.write(row,14,"")

            worksheet.write(row, 15, child_dic["image_url"])
            
            #other images 
            worksheet.write(row,16, parent_dic["i1"])
            worksheet.write(row,17, parent_dic["i2"])
            worksheet.write(row,18, parent_dic["i3"])
            worksheet.write(row,19, parent_dic["i4"])
            worksheet.write(row,20, parent_dic["i5"])
            worksheet.write(row,21, parent_dic["i6"])
            worksheet.write(row,22, parent_dic["i7"])
    workbook.close()          