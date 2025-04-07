from djangoTSGems.products.models import (
    DropEarring,
    StudEarring,
    Necklace,
    Pendant,
    Charm,
    Bracelet,
    Ring
)

products_by_size_and_price = [
    {
        'class': Charm,
        'sizes': [1.6],
        'prices': [3000],
    },
    {
        'class': Pendant,
        'sizes': [39.53, 41.64, 44.18, 46.72, 48.46],
        'prices': [33000, 34000, 35000, 36000, 37000],
    },
    {
        'class': StudEarring,
        'sizes': [0.51],
        'prices': [6000],
    },
    {
        'class': Bracelet,
        'sizes': [13.1, 15.2, 17.8, 19.3, 20.2],
        'prices': [16000, 17000, 18000, 19000, 20000],
    },
    {
        'class': Ring,
        'sizes': [3.04, 4.05, 4.98, 5.86, 6.34],
        'prices': [11000, 12000, 13000, 14000, 15000],
    },
    {
        'class': Necklace,
        'sizes': [38.53, 40.64, 43.18, 45.72, 47.46],
        'prices': [39000, 40000, 41000, 42000, 43000],
    },
    {
        'class': DropEarring,
        'sizes': [4.6],
        'prices': [22000],
    },
]

products_by_images_and_description = {
    'Charm': {
        'PS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957286/forget_me_not_charm_diamond_and_pink_sapphire_cmpsprfflrfmn_e-1_f3fwf3_sj5caa.avif',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957291/forget_me_not_charm_diamond_and_pink_sapphire_cmpsprfflrfmn_e-2_xteknd_h3qsgy.avif',
            'description': '6 pear-shaped pink sapphires weighing a total of approximately 0.84 carats and 1 round brilliant diamond weighing approximately 0.03 carats, set in platinum'
        },
        'BS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957291/forget_me_not_charm_diamond_and_sapphire_cmsprfflrfmn_e-1_cgsrfu_vcmbt4.avif',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957292/forget_me_not_charm_diamond_and_sapphire_cmsprfflrfmn_e-2_utcyi1_ooankh.avif',
            'description': '6 pear-shaped sapphires weighing a total of approximately 0.81 carats and 1 round brilliant diamond weighing approximately 0.03 carats, set in platinum'
        },
        'BD': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957287/forget_me_not_diamond_charm_cmdprfflrfmn_e-1_pvbm1i_my4io5.avif',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957291/forget_me_not_diamond_charm_cmdprfflrfmn_e-2_quxwi3_jz6dme.avif',
            'description': '6 pear-shaped and 1 round brilliant diamond weighing a total of approximately 0.60 carats, set in platinum'
        }
    },
    'Pendant': {
        'PS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957270/forget_me_not_pendant_diamond_and_pink_sapphire_pepsprfflrfmn_e_1_ddzgzr_rm1pic.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957270/forget_me_not_pendant_diamond_and_pink_sapphire_pepsprfflrfmn_e_2_alppwn_i4obp0.avif',
            'description': '6 pear-shaped pink sapphires weighing a total of approximately 1.44 carats and 1 round brilliant diamond weighing approximately 0.04 carats, set in platinum'
        },
        'BS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957270/forget_me_not_pendant_diamond_and_sapphire_pesprfflrfmn_e_1_igv8vt_cwzbae.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957269/forget_me_not_pendant_diamond_and_sapphire_pesprfflrfmn_e_2_xyhpns_ujue4d.avif',
            'description': '6 pear-shaped sapphires weighing a total of approximately 1.41 carats and 1 round brilliant diamond weighing approximately 0.04 carats, set in platinum'
        },
        'BD': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957270/forget_me_not_diamond_pendant_pedprfflrfmn_e-1h_ijqoqu_qcgffw.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957270/forget_me_not_diamond_pendant_pedprfflrfmn_e-2h_xdbhby_z7ltdd.webp',
            'description': '6 pear-shaped and 1 round brilliant diamond weighing a total of approximately 1.07 carats, set in platinum'
        }
    },
    'StudEarring': {
        'PS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957286/forget_me_not_earrings_diamond_and_pink_sapphire_eapsp1mflrfmn_ee-1_z57oqb_u5wgnp.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957283/forget_me_not_earrings_diamond_and_pink_sapphire_eapsp1mflrfmn_ee-2_fdeq4k_uqkvie.webp',
            'description': '12 pear-shaped pink sapphires weighing a total of approximately 2.20 carats and 2 round brilliant diamonds weighing a total of approximately 0.07 carats, set in platinum'
        },
        'BS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957283/forget_me_not_earrings_diamond_and_sapphire_easp1mflrfmn_ee-1_bczp2o_ng3k9z.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957285/forget_me_not_earrings_diamond_and_sapphire_easp1mflrfmn_ee-2_zkymsa_gjhd90.webp',
            'description': '12 pear-shaped sapphires weighing a total of approximately 2.10 carats and 2 round brilliant diamonds weighing a total of approximately 0.07 carats, set in platinum'
        },
        'BD': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957286/forget_me_diamond_earrings_eadp1mflrfmn_ee-1_vpnnjq_rbld9s.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957287/forget_me_not_diamond_earrings_eadp1mflrfmn_ee-2_bldtfr_kxrqnr.webp',
            'description': '12 pear-shaped diamonds and 2 round brilliant diamonds weighing a total of approximately 1.70 carats, set in platinum'
        }
    },
    'Bracelet': {
        'PS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957299/forget_me_not_bracelet_diamond_and_pink_sapphire_brpsprfflrfmn_e_1_vz9pv4_ojgh1x.avif',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957296/forget_me_not_bracelet_diamond_and_pink_sapphire_brpsprfflrfmn_e_2_kdpnm6_c8locj.avif',
            'description': '45 pear-shaped and round brilliant pink sapphires weighing a total of approximately 4.36 carats and 33 pear-shaped, marquise and round brilliant diamonds weighing a total of approximately 4.24 carats, set in platinum'
        },
        'BS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957297/forget_me_not_bracelet_diamond_and_sapphire_brsprfflrfmn_e_1_fokzrw_gpf0s4.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957298/forget_me_not_bracelet_diamond_and_sapphire_brsprfflrfmn_e_2_ojfbze_amxejs.avif',
            'description': '45 pear-shaped and round brilliant sapphires weighing a total of approximately 4.17 carats and 33 pear-shaped, marquise and round brilliant diamonds weighing a total of approximately 4.24 carats, set in platinum'
        },
        'BD': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957299/forget_me_not_diamond_bracelet_brdprfflrfmn_e-1_muieri_xwqirj.avif',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957297/forget_me_not_bracelet_diamond_and_pink_sapphire_brpsprfflrfmn_e_2_1_pvbpcb_rxum0y.png',
            'description': '78 pear-shaped, marquise, and round brilliant diamonds, weighing a total of approximately 7.46 carats, set in platinum'
        }
    },
    'Ring': {
        'PS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957295/forget_me_not_ring_diamond_and_pink_sapphire_frpsprfflrfmn_e_1_qfumu3_tkws9f.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957296/forget_me_not_ring_diamond_and_pink_sapphire_frpsprfflrfmn_e_2_k7nhpe_ay3lie.avif',
            'description': '6 pear-shaped pink sapphires weighing a total of approximately 2.22 carats and 1 round brilliant diamond weighing approximately 0.05 carats, set in platinum'
        },
        'BS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957296/forget_me_not_ring_diamond_and_sapphire_frsprfflrfmn_e_1_pm9u6t_b3euoo.avif',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957296/forget_me_not_ring_diamond_and_sapphire_frsprfflrfmn_e_2_ucppcd_z5coh7.avif',
            'description': '6 pear-shaped sapphires weighing a total of approximately 2.15 carats and 1 round brilliant diamond weighing approximately 0.05 carats, set in platinum'
        },
        'BD': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957295/forget_me_not_diamond_ring_frdprfflrfmn_e-1h_yueh2k_xasnpi.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957295/forget_me_not_diamond_ring_frdprfflrfmn_e-2h_mktny9_ith5pb.webp',
            'description': '6 pear-shaped and 1 round brilliant diamond, weighing a total of approximately 1.66 carats, set in platinum'
        }
    },
    'Necklace': {
        'PS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957294/forget_me_not_lariat_necklace_diamond_and_pink_sapphire_nkpspltflrfmn_e_1_kuxbds_h3z6kz.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957294/forget_me_not_lariat_necklace_diamond_and_pink_sapphire_nkpspltflrfmn_e_2_d2fc78_nf6ni1.webp',
            'description': '78 pear-shaped and round brilliant pink sapphires weighing a total of approximately 8.61 carats and 99 marquise and round brilliant diamonds weighing a total of approximately 8.60 carats, set in platinum'
        },
        'BS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957294/forget_me_not_lariat_necklace_diamond_and_sapphire_nkspltflrfmn_e_1_p2uxlj_hqfg4a.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957294/forget_me_not_lariat_necklace_diamond_and_sapphire_nkspltflrfmn_e_2_hxgdcy_vf9epk.avif',
            'description': '78 pear-shaped and round brilliant sapphires weighing a total of approximately 8.61 carats and 99 marquise and round brilliant diamonds weighing a total of approximately 8.37 carats, set in platinum'
        },
        'BD': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957294/forget_me_not_lariat_diamond_necklace_nkdpltflrfmn_e-1_u0gwpv_jv0o2i.avif',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957292/forget_me_not_lariat_diamond_necklace_nkdpltflrfmn_e-2_tuh8ru_acwgee.webp',
            'description': '177 pear-shaped, marquise, and round brilliant diamonds, weighing a total of approximately 15.35 carats, set in platinum'
        }
    },
    'DropEarring': {
        'PS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957283/forget_me_not_drop_earrings_diamond_and_pink_sapphire_eapspdrflrfmn_ee-1_zzaw4q_yqmref.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957283/forget_me_not_drop_earrings_diamond_and_pink_sapphire_eapspdrflrfmn_ee-2_p9jicb_aedtpz.webp',
            'description': '28 pear-shaped and round brilliant pink sapphires weighing a total of approximately 3.20 carats and 28 marquise and round brilliant diamonds weighing a total of approximately 1.98 carats, set in platinum'
        },
        'BS': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957283/forget_me_not_drop_earrings_diamond_and_sapphire_easpdrflrfmn_ee-1_zx2cga_fuwje2.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957281/forget_me_not_drop_earrings_diamond_and_sapphire_easpdrflrfmn_ee-2_vtkyhb_g8xu2n.webp',
            'description': '28 pear-shaped and round brilliant sapphires weighing a total of approximately 3.00 carats and 28 marquise and round brilliant diamonds weighing a total of approximately 1.98 carats, set in platinum'
        },
        'BD': {
            'first_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957281/forget_me_not_diamond_drop_earrings_eadpdrflrfmn_ee-1_knlt2u_wcd0o9.webp',
            'second_image_url': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957280/forget_me_not_diamond_drop_earrings_eadpdrflrfmn_ee-2_sksk7o_jkcjag.webp',
            'description': 'A medley of marquise, pear-shaped, and round brilliant diamonds, weighing a total of approximately 4.38 carats, set in platinum'
        }
    }
}
