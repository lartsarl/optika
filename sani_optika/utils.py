def handle_uploaded_file(f, filename):
    with open('sani_optika/static/sani_optika/images/review/' + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
