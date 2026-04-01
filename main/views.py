from django.shortcuts import render

def index(request):
    data_biodata = [
        {
            "nama": "Davin Fauzan", 
            "umur": 19, 
            "npm" : "2406409504",
            "prodi": "Ilmu Komputer", 
            "gambar": "/static/image/davin.png"
        },
        {
            "nama": "Peter Yap", 
            "umur": 19, 
            "npm": "2406432910",
            "prodi": "Ilmu Komputer", 
            "gambar": "/static/image/peter.jpg"
        },
        {
            "nama": "Farrell Bagoes Rahmantyo", 
            "umur": 21, 
            "npm": "2406420596", 
            "prodi": "Ilmu Komputer",
            "gambar": "/static/image/farrell.jpg"
        },
        {
            "nama": "Andrew Wanarahardja", 
            "umur": 19, 
            "npm": "2406407373",
            "prodi": "Ilmu Komputer", 
            "gambar": "/static/image/andrew.png"
        },
		{
			"nama": "Rousan Chandra Syahbunan", 
			"umur": 69, 
			"npm": "2406435894",
			"prodi": "Ilmu Komputer", 
			"gambar": "/static/image/rousan.jpg"
		},
    ]
    return render(request, "main/index.html", {"biodata_list": data_biodata})