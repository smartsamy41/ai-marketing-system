def count_product_schema(html: str) -> int:

    if not html:
        return 0

    return html.count(
        '"@type": "Product"'
    )



def schema_status(html: str) -> dict:

    count = count_product_schema(
        html
    )

    return {

        "product_schema_count":
            count,

        "status":
            "OK"
            if count <= 2
            else "DUPLICATE_WARNING"

    }



if __name__ == "__main__":

    test = '''
    {
      "@type": "Product"
    }
    '''

    print(
        schema_status(test)
    )
