from watermark import Watermark

watermarked = Watermark("C:\\Users\\svitale\\Downloads\\2015-06-12 14_29_58-Postman.png")
watermarked.apply_text("\xa9 Vitale's Studio", tile=True)
watermarked.save("C:\\Users\\svitale\\Downloads\\2015-06-12 14_29_58-Postman - watermark.png")
