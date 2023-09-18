scholarlyarticle = {
    "type": "object",
    "properties": {
        "@context": {"type": "string"},
        "@type": {"type": "string"},
        "name": {"type": "string"},
        "headline": {"type": "string"},
        "description": {"type": "string"},
        "datePublished": {"type": "string"},
        "dateModified": {"type": "string"},
        "keywords": {"type": "string"},
        "author": [
        {
            "@type": {"type": "string"},
            "name": {"type": "string"}
        },
        {
            "@type": {"type": "string"},
            "name": {"type": "string"}
        }
        ],
        "publisher": {
        "@type": {"type": "string"}, 
        "name": {"type": "string"},
        "logo": {
            "@type": {"type": "string"},
            "url": {"type": "string"},
            "width": {"type": "number"},
            "height": {"type": "number"}
        }
        },
        "url": {"type": "string"},
        "image": {"type": "array", "items": {"type": "array", "items": {
            "@type": {"type": "string"},
            "url": {"type": "string"},
            "width": {"type": "number"},
            "height": {"type": "number"}
        }
        
        },
        "isPartOf": {
        "@type": {"type": "string"},
        "name": {"type": "string"},
        "issn": {"type": "string"}
        },
        "pagination": {"type": "string"},
        "articleSection": {"type": "string"},
        "pageStart": {"type": "string"},
        "pageEnd": {"type": "string"},
        "volumeNumber": {"type": "string"},
        "issueNumber": {"type": "string"},
        "identifier": [
        {
            "@type": {"type": "string"},
            "propertyID": {"type": "string"},
            "value": {"type": "string"}
        },
        {
            "@type": {"type": "string"},
            "propertyID": {"type": "string"},
            "value": {"type": "string"}
        }
        ],
        "citation": {
        "@type": {"type": "string"},
        "author": [
            {
            "@type": {"type": "string"},
            "name": {"type": "string"}
            },
            {
            "@type": {"type": "string"},
            "name": {"type": "string"}
            }
        ],
        "name": {"type": "string"},
        "datePublished": {"type": "string"},
        "publisher": {"type": "string"}
        }
}
    }
}