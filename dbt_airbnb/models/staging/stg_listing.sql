with source as (
    select * from {{ source('raw_data', 'raw_listings') }}
),

renamed as (
    select
        id as listing_id,
        name as listing_name,
        description as listing_description,
        neighborhood_overview as neighborhood
        host_id,
        host_name,
        host_profile_id,
        room_type,
        accommodates,
        bedrooms,
        beds,
        -- Nettoyage du prix : "$150.00" -> 150.00
        cast(replace(replace(price, '$', ''), ',', '') as double) as price_night,
        minimum_nights,
        maximum_nights,
        number_of_reviews,
        review_scores_rating as rating
    from source
)

select * from renamed
