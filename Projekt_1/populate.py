import os

def populate():
	add_zawod("Gornik")
	add_zawod("Informatyk")
	add_zawod("Elektryk")
	add_zawod("Inny")
	add_zawod("Geodeta")
	
	add_obywatelstwo("Polska")
	add_obywatelstwo("Niemcy")
	add_obywatelstwo("Inny")
	
	add_kategoria("Prezydenckie")
	add_kategoria("Samorzadowe")
	add_kategoria("Inne")
	
	
    # Print out what we have added to the user.
    #for z in Zawod.objects.all():
    #	print "%s" % z
    #for o in Obywatelstwo.objects.all():
    #	print "%s" % o
    #for k in Kategoria.objects.all():
    #	print "%s" %k

def add_zawod(name):
    z = Zawod.objects.get_or_create(nazwa=name)[0]
    return z
    
def add_obywatelstwo(country):
	o = Obywatelstwo.objects.get_or_create(kraj=country)[0]
	return o
	
def add_kategoria(category):
	c = Kategoria.objects.get_or_create(nazwa=category)[0]
	return c
	
# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projekt_1.settings')
    from mainapp.models import Zawod, Obywatelstwo, Kategoria
    populate()
