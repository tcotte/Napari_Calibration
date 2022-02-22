import cv2
import matplotlib.pyplot as plt


def get_hypothenuse(x, y):
    return x ** 2 + y ** 2


def pixel_per_mm(px, cm):
    return px / cm


def get_str_length(len, ratio):
    length = len / ratio
    return "{:.2f}".format(length)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(get_hypothenuse())
    ratio = pixel_per_mm(1813.06, 7)

    img = cv2.imread("img/carre.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("gray.png", gray)
    blur = cv2.blur(gray, (50, 50), 0)
    ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    plt.imshow(thresh, cmap="gray")
    plt.show()

    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    idx = 0

    output = img.copy()
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w > 600 and h > 600:
            idx += 1

            start_point = (x, y)
            end_point = (x + w, y + h)

            output = cv2.rectangle(img, start_point, end_point, (0, 255, 0), 5)
            cv2.putText(output, "w = " + get_str_length(w, ratio) + " cm", (x + 40, y - 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 10,
                        (0, 255, 0), 10)
            cv2.putText(output, "h = " + get_str_length(h, ratio) + " cm", (x + 40, y - 300), cv2.FONT_HERSHEY_COMPLEX_SMALL, 10,
                        (0, 255, 0), 10)

            print(w / ratio)
            print(h / ratio)
    plt.imshow(output)
    plt.show()
