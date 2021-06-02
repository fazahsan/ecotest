from django.shortcuts import render, redirect
import pythoncom
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View

from store.models.product import Product
from store.models.orders import Order
import win32com.client  as client
import pandas as pd
import xlsxwriter
import pathlib

pythoncom.CoInitialize()

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)
        seninfo = {'Order': [], 'Cantidad': [], 'Precios': []}
        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            seninfo["Order"].append(order.product.name)
            seninfo["Cantidad"].append(order.quantity)
            seninfo["Precios"].append(order.product.price)
            order.save()


        request.session['cart'] = {}
        Total=0
        for precio in seninfo['Precios']:
            Total=Total+precio

        #print(' here are orders',order.product.name,order.product.category)
        if request.POST.get('csv'):
            print('length',len (seninfo ))
            info = pd.DataFrame(seninfo)
            avg_row = ['Total a pagar son', '  ',Total]
            info.loc[len(info)] = avg_row
            pythoncom.CoInitialize()
            info.to_csv(r'demo.csv', index=False, header=True)
            cart1_path = pathlib.Path('demo.csv')
            cart1 = str(cart1_path.absolute())
            outlook = client.Dispatch("Outlook.Application")
            message = outlook.CreateItem(0)
            message.Display()
            message.subject = 'Hello'
            message.SendUsingAccount = 
            # email where you want to recive order
            message.To = 
            message.Body = 'pedido de cliente '
            message.Attachments.Add(cart1)
            message.Send()
            return redirect('store')
        else:

            pythoncom.CoInitialize()
            info = pd.DataFrame(seninfo)
            avg_row = ['Total a pagar son ', '   ',Total]
            info.loc[len(info)] = avg_row
            writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
            info.to_excel(writer, sheet_name='Sheet1', index=False)
            writer.save()
            cart1_path = pathlib.Path('demo.xlsx')
            cart1 = str(cart1_path.absolute())
            print('yhis is the path', cart1)
            outlook = client.Dispatch("Outlook.Application")
            message = outlook.CreateItem(0)
            message.Display()
            message.subject = 'Hello'
            message.SendUsingAccount = 
            # email where you want to recive order
            message.To = 
            message.Body = 'pedido del cliente '

            message.Attachments.Add(cart1)
            message.Send()
            return redirect('cart')

