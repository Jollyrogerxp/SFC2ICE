import argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("sfcfile", help="filename of sfc file to be converted")
    parser.add_argument("--hirom", help="treat input sfc file as hirom", action="store_true")
    args = parser.parse_args()

    split_filename = os.path.splitext(args.sfcfile)
    base_filename = split_filename[0]

    base_filename = (base_filename[:6]) if len(base_filename) > 6 else base_filename

    if args.hirom:

        # load the sfc binary
        # split into 32k blocks and save them as separate binary files
        # compose the ICE file

        sfc_file = open(args.sfcfile, "rb")
        ice_file = open(base_filename + ".ICE", "w")

        # read every other 32k page

        pages = []

        page = sfc_file.read(32768)

        while page:
            pages.append(page)
            page = sfc_file.read(32768)

        sfc_file.close()

        # store every second half page in separate files

        counter = 0

        for page_index in range(1, len(pages), 2):
            txt = base_filename + "{page:02x}.BIN"
            rbn_filename = txt.format(page=page_index)

            rbn_file = open(rbn_filename, "wb")
            rbn_file.write(pages[page_index])
            rbn_file.close()

            txt = ",{page:02x}:8000"
            ice_file.write("R " + rbn_filename + txt.format(page=counter) + '\n')

            counter = counter + 1


        # store all full 64k pages in separate files

        counter = 0

        for page_index in range(0, len(pages), 2):
            txt = base_filename + "{page:02x}.BIN"
            rbn_filename = txt.format(page=page_index)

            rbn_file = open(rbn_filename, "wb")
            rbn_file.write(pages[page_index])
            rbn_file.write(pages[page_index+1])
            rbn_file.close()

            txt = ",{page:02x}:0000"

            if counter > 0x3D:
                ice_file.write("R " + rbn_filename + txt.format(page=counter+0xC0) + '\n')
            else:
                ice_file.write("R " + rbn_filename + txt.format(page=counter+0x40) + '\n')

            counter = counter + 1

        # write the reset and start commands

        ice_file.write("Z\n")
        ice_file.write("G\n")

        ice_file.close()

    else:

        # load the sfc binary
        # split into 32k blocks and save them as separate binary files
        # compose the ICE file

        sfc_file = open(args.sfcfile, "rb")
        ice_file = open(base_filename + ".ICE", "w")

        page = sfc_file.read(32768)

        counter = 0

        while page:
            txt = base_filename + "{page:02x}.BIN"
            rbn_filename = txt.format(page=counter)

            rbn_file = open(rbn_filename, "wb")
            rbn_file.write(page)
            rbn_file.close()

            txt = ",{page:02x}:8000"
            if counter > 0x7D:
                ice_file.write("R " + rbn_filename + txt.format(page=counter+0x80) + '\n')
            else:
                ice_file.write("R " + rbn_filename + txt.format(page=counter) + '\n')


            page = sfc_file.read(32768)

            counter = counter + 1

        ice_file.write("Z\n")
        ice_file.write("G\n")

        sfc_file.close()
        ice_file.close()

